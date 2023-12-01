from datetime import timedelta
import logging
from firebase_admin import storage
from kuhub.models import Profile


LOGGER = logging.getLogger('kuhub')

def separate_folder_firebase(folder: str):
    """Retrieve signed URLs for files in a specified Firebase Storage folder."""
    try:
        bucket = storage.bucket()
        blobs = bucket.list_blobs(prefix=folder)
        file_store = {}
        for blob in blobs:
            # Generate a signed URL for each file
            if not blob.name.endswith('/'):
                signed_url = blob.generate_signed_url(
                    expiration=timedelta(seconds=300))
                delete_folder = blob.name.replace(folder, '')
                file_store[delete_folder] = signed_url
    except ValueError:
        return {}

    return file_store


def navbar_setting_profile(request):
    """ Set the user's profile photo based on a signed URL from Firebase Storage."""
    try:
        display_photo_key = request.user.profile.display_photo
        if display_photo_key is not None:
            photo_dict = separate_folder_firebase('profile/')
            if display_photo_key in photo_dict:
                request.user.profile.display_photo = photo_dict[
                    display_photo_key]
            else:
                # Handle the case where the key doesn't exist
                Profile.objects.filter(user=request.user).update(
                    display_photo='default_profile_picture.png')

    except (AttributeError, KeyError) as e:
        # Log the error or handle it appropriately
        LOGGER.error(
            f'Error setting profile photo for user '
            f'{request.user.username}: {e}'
        )
        return None
