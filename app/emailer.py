import base64
from email.message import EmailMessage
from os import getenv, path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]


def get_credentials():
    creds = None
    if path.exists('../token.json'):
        creds = Credentials.from_authorized_user_file('../token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('../token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def send_email(message):
    creds = get_credentials()
    try:
        service = build('gmail', 'v1', credentials=creds)

        email = EmailMessage()
        email.set_content(message)
        email['To'] = getenv('RECEIVER_EMAIL')
        email['From'] = getenv('SENDER_EMAIL')
        email['Subject'] = 'Auto Renewer'

        # encode and send email
        encoded_message = base64.urlsafe_b64encode(email.as_bytes()).decode()
        create_message = {
            'raw': encoded_message
        }
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message
