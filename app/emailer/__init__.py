import os
import pickle
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64encode
# for dealing with attachment MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

from app.utlis.settings import config
from app.utlis.constants import GMAIL_SCOPES


sender_email_address = config['SENDER_EMAIL_ADDRESS']


class Emailer:
    def __init__(self):
        # get the Gmail API service
        self.service = self.__gmail_authenticate()

    @staticmethod
    def __gmail_authenticate():
        creds = None
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", GMAIL_SCOPES)
                creds = flow.run_local_server(port=0)
            # save the credentials for the next run
            with open("token.pickle", "wb") as token:
                # noinspection PyTypeChecker
                pickle.dump(creds, token)
        return build('gmail', 'v1', credentials=creds)

    @staticmethod
    def __add_attachment(message, filename):
        # Adds the attachment with the given filename to the given message
        content_type, encoding = guess_mime_type(filename)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(filename, 'rb')
            msg = MIMEText(fp.read().decode(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(filename, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(filename, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(filename, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
        filename = os.path.basename(filename)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

    def __build_message(self, destination: str, subject: str, body: str, attachments: str|None=None):
        if attachments is None:
            attachments = []
        if not attachments:
            message = MIMEText(body)
            message['to'] = destination
            message['from'] = sender_email_address
            message['subject'] = subject
        else:
            message = MIMEMultipart()
            message['to'] = destination
            message['from'] = sender_email_address
            message['subject'] = subject
            message.attach(MIMEText(body))
            for filename in attachments:
                self.__add_attachment(message, filename)
        return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}

    def send_message(self, destination, obj, body, attachments=None):
        return self.service.users().messages().send(
            userId="me",
            body=self.__build_message(destination, obj, body, attachments)
        ).execute()
