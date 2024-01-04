import json
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from openai import OpenAI

# Read configuration file for API keys
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    openai_api_key = config['openai_api_key']

# Scopes and OAuth 2.0 Credentials File
SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'path/to/credentials.json'
CALENDAR_ID = 'primary'  # or your calendar ID

def get_calendar_service():
    creds = None
    # Load the saved credentials if they exist
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no valid credentials, prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

# Initialize the Google Calendar API client using OAuth
service = get_calendar_service()

client = OpenAI(api_key=openai_api_key)

def add_calendar_event(event_summary, event_location, event_description, start_time, end_time, start_time_zone, end_time_zone):
    """
    Adds an event to the Google Calendar.
    """
    event = {
        'summary': event_summary,
        'location': event_location,
        'description': event_description,
        'start': {
            'dateTime': start_time,
            'timeZone': start_time_zone,
        },
        'end': {
            'dateTime': end_time,
            'timeZone': end_time_zone,
        },
    }
    try:
        event_result = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        return f"Event created: {event_result.get('htmlLink')}"
    except Exception as e:
        return f"An error occurred: {e}"

def provide_user_specific_recommendations():
    messages = [
        {"role": "system", "content": "You are an AI that schedules events in a Google Calendar."},
        {"role": "user", "content": "Schedule a meeting with John on January 10 at 10 am."}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        functions=[
            {
                "name": "add_calendar_event",
                "description": "Add an event to Google Calendar",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "event_summary": {"type": "string"},
                        "event_location": {"type": "string"},
                        "event_description": {"type": "string"},
                        "start_time": {"type": "string"},
                        "end_time": {"type": "string"},
                        "start_time_zone": {"type": "string"},
                        "end_time_zone": {"type": "string"},
                    },
                    "required": ["event_summary", "event_location", "event_description", "start_time", "end_time", "start_time_zone", "end_time_zone"],
                }
            }
        ]
    )

    if response.choices[0].finish_reason == 'function_call':
        function_call = response.choices[0].message.function_call
        if function_call.name == "add_calendar_event":
            args = json.loads(function_call.arguments)
            return add_calendar_event(args['event_summary'], args['event_location'], args['event_description'], args['start_time'], args['end_time'], args['start_time_zone'], args['end_time_zone'])

    return "I am sorry, but I could not understand your request."

if __name__ == "__main__":
    output = provide_user_specific_recommendations()
    print(output)
