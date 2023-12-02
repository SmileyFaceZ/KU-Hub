"""This module provides functionality for interacting with Firebase storage."""
from firebase_admin import storage
from datetime import timedelta
import re
import os
from isp_project import settings


class FirebaseFolder:
    """Firebase folder class pulls files from firebase storage."""

    @staticmethod
    def separate_folder_firebase(folder: str) -> dict:
        """Separate folder from firebase and return a dictionary of files.

        :param: folder (str): The folder path in Firebase storage.
        :return: A dictionary where keys are file names
        and values are signed URLs for these files.
        """
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
            return {
                'default_profile_picture.png':
                    'https://firebasestorage.googleapis.com/v0/b/ku-hub-76621'
                    '.appspot.com/o/profile%2Fdefault_profile_picture.png?'
                    'alt=media&token=0016bd21-2f03-4ff0-ab6f-c54401c8392c'}

        return file_store

    @staticmethod
    def file_handling(photo: str):
        """To handles the deletion of a file from the media directory.

        :param: photo: The file name of the photo to be handled.
        """
        clean_file_name = re.sub(r'\s+', '_', photo)
        clean_file_name = re.sub(r'[()]', '', clean_file_name)
        clean_file_path = os.path.join(
            settings.MEDIA_ROOT,
            clean_file_name)

        # Remove file from media directory
        if os.path.exists(clean_file_path):
            os.remove(clean_file_path)
