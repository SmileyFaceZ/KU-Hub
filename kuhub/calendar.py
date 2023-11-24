from django.shortcuts import redirect
from google.oauth2.credentials import Credentials
from allauth.socialaccount.models import SocialToken
from googleapiclient.discovery import build
from google.oauth2 import service_account
from kuhub.models import group_event


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

def create_calendar(request, name):
    service = get_google_calendar_service(request)
    new_calendar = {
        'summary': name,
        'timeZone': 'Asia/Bangkok'
    }
    created_calendar = service.calendars().insert(body=new_calendar).execute()
    return created_calendar

def add_participate(user, calendar_id):
    """
    add user to can edit the group's calendar
    """
    try:
        service = get_service_by_service_account()
        service.acl().insert(calendarId=calendar_id,
                             body={'role': 'owner',
                                   'scope': {'type': 'group',
                                             'value': user.email
                                             }}).execute()
    except user.email.DoesNotExist:
        print("email does not exists")


def create_event(request ,summary ,location, start_datetime, end_datetime, description):
    """
    Create a new event in the User's Google Calendar.
    """
    service = get_google_calendar_service(request)

    group_event.GroupEvent
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
        }

        created_event = service.events().insert(calendarId='primary', body=event,conferenceDataVersion=1).execute()
        return created_event


def generate_meeting(request, eventobj, event_id):
    service = get_google_calendar_service(request)
    reqid = eventobj.generate_request_id()
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    event['conferenceData'] = {'createRequest': {
                                    'requestId': reqid,
                                    'conferenceSolutionKey': {
                                            'type': 'hangoutsMeet'
                                            }
                                    }
                                }

    updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
    return updated_event

def delete_event(request ,event_id):
    service = get_google_calendar_service(request)
    service.events().delete(calendarId='primary', eventId=event_id).execute()
