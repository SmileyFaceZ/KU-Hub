from django.http import HttpResponse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from allauth.socialaccount.models import SocialToken
from googleapiclient.discovery import build
from google.oauth2 import service_account

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
            "client_id": "298266224776-o5thmj41tjhabonol6nf853qt9f8np7l.apps.googleusercontent.com",
            "client_secret": "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",
            "refresh_token": str(access_token),
        }
    credentials = Credentials.from_authorized_user_info(info=user_info,scopes=scope)
    service = build('calendar', 'v3', credentials=credentials)
    return service

def get_service_by_service_account():
    """
        Create and return a Google Calendar API service instance using the provided credentials.
        With google service account.
    """
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    # Load the service account credentials
    credentials = service_account.Credentials.from_service_account_file(
        'data/ku-hub-403109-d333bb4ea845.json',
        scopes=SCOPES
    )

    # Create a service object
    service = build('calendar', 'v3', credentials=credentials)
    return service

def create_calendar(name):
    service = get_service_by_service_account()
    new_calendar = {
        'summary': name,
        'timeZone': 'Asia/Bangkok'
    }
    created_calendar = service.calendars().insert(body=new_calendar).execute()
    return created_calendar

def create_event(request, summary, start_datetime, end_datetime):
    """
    Create a new event in the user's Google Calendar.
    """
    service = get_google_calendar_service(request)

    if service:
        event = {
            'summary': summary,
            'start': {'dateTime': start_datetime, 'timeZone': 'Asia/Bangkok'},
            'end': {'dateTime': end_datetime, 'timeZone': 'Asia/Bangkok'},
        }

        created_event = service.events().insert(calendarId='primary', body=event).execute()
        return created_event  # You might want to handle the response in your views
