import datetime as dt
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters,ContextTypes


from datetime import timezone


SCOPES = ["https://www.googleapis.com/auth/calendar"]



class GoogleCalendarManager:
    def __init__(self):
        self.service = self.authenticate()
        self.calendarId = "8b30dc82db66a8738b9f6845ef502f9857c7f4cd779109119d02fc448bef36f3@group.calendar.google.com"

    def authenticate(self):
        service_account_file = "client_secret.json"

        self.credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=SCOPES
        )
        self.service = build('calendar', 'v3', credentials=self.credentials)
        return self.service
    
    def list_upcoming_events(self, max_results=100):

        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indica UTC


        events_result = self.service.events().list(
            calendarId=self.calendarId,
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        event_list = []
        if not events:
            event_list.append('No upcoming events found.')
        else:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                summary = event.get('summary', 'No Title')

                # Convertir las fechas y horas a objetos datetime
                start_dt = datetime.fromisoformat(start)
                end_dt = datetime.fromisoformat(end)

                start_date = start_dt.strftime('%Y-%m-%d')
                start_time = start_dt.strftime('%H:%M')
                end_time = end_dt.strftime('%H:%M')

                event_list.append(f"Fecha: {start_date} Desde: {start_time} Hasta: {end_time} - {summary}")

        return event_list
            

        


    def create_event(self, summary, start_time, end_time, timezone, attendees=None):
        event = {
            'summary':summary,
            'start': {
                'dateTime': start_time,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time,
                'timeZone': timezone,
            }
        }

        if attendees:
            event['attendees'] == [{'email': email} for email in attendees]

        try:
            event = self.service.events().insert(calendarId= self.calendarId, body=event).execute()

            print(f"Event created: {event.get('htmlLink')}")

        except HttpError as error:
            print(f"A ocurrido un error: {error}")


    def update_event(self, event_id, summary=None, start_time= None, end_time=None):
        event = self.service.events().get(calendarId=self.calendarId, eventId=event_id).execute()

        if summary:
            event['summary'] = summary
        if start_time:
            event['start']['dateTime'] = start_time.strftime(f"%Y-%m-%dT%H:%M:%S")
        if end_time:
            event['end']['dateTime'] = end_time.strftime(f"%Y-%m-%dT%H:%M:%S")
        
        update_event = self.service.events().update(
            calendarId=self.calendarId, eventId=event_id, body=event
        ).execute()

        return update_event

    def delete_event(self, event_id):
        self.service.events().delete(calendarId=self.calendarId, eventId=event_id).execute()
        return True


    def is_time_slot_available(self, start_time, end_time):

        
        start_time_utc = start_time.astimezone(timezone.utc)
        end_time_utc = end_time.astimezone(timezone.utc)

        print(f"Checking availability from {start_time.isoformat()} to {end_time.isoformat()}")

        events_result = self.service.events().list(
            calendarId=self.calendarId,
            timeMin=start_time_utc.isoformat(),
            timeMax=end_time_utc.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        print(f"Found {len(events)} events")


        for event in events:
            print(f"Event: {event['summary']} from {event['start']['dateTime']} to {event['end']['dateTime']}")
            
            # Check if the requested time slot overlaps with any existing events
            existing_start = datetime.fromisoformat(event['start']['dateTime'])
            existing_end = datetime.fromisoformat(event['end']['dateTime'])

            if (start_time < existing_end and end_time > existing_start):
                return False

        return len(events) == 0