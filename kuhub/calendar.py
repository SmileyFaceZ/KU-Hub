import uuid

from google.oauth2.credentials import Credentials
from allauth.socialaccount.models import SocialToken
from googleapiclient.discovery import build
from decouple import config


def get_google_calendar_service(request):
    """
    Create and return a Google Calendar API service instance using the provided credentials.
    """
    user = request.user
    try:
        social_token = SocialToken.objects.get(account__user=user, account__provider='google')
        access_token = social_token.token
    except SocialToken.DoesNotExist:
        # Handle the case where the user hasn't connected their Google account
         return None
    scope = ['https://www.googleapis.com/auth/calendar']
    user_info = {
            "client_id": config('GOOGLE_OAUTH_CLIENT_ID', default='google-oauth-client-id'),
            "client_secret": config('GOOGLE_OAUTH_SECRET_KEY', default='google-oauth-secret-key'),
            "refresh_token": str(access_token),
        }
    credentials = Credentials.from_authorized_user_info(info=user_info,scopes=scope)
    service = build('calendar', 'v3', credentials=credentials)
    return service


def create_event(request, summary, location, start_datetime, end_datetime, description):
    """
    Create a new event in the User's Google Calendar.
    """
    service = get_google_calendar_service(request)

    if service:
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_datetime,
                'timeZone': 'Asia/Bangkok'
            },
            'end': {
                'dateTime': end_datetime,
                'timeZone': 'Asia/Bangkok'
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': str(uuid.uuid4()),
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    }
                }
            }
        }

        created_event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()

        # Retrieve Hangouts Meet link
        meet_link = created_event.get('conferenceData', {}).get('entryPoints', [])[0].get('uri', '')

        return created_event, meet_link

    return None, None, None
