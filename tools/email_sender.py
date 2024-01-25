from __future__ import print_function
import base64
import logger
import os.path
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']
TOKEN_FILE = os.path.join(os.path.expanduser('~'), '.credentials', 'gmail_token.json')
CLIENT_SECRET_FILE = os.path.join(os.path.expanduser('~'), '.credentials', 'gmail_client_secret.json')

logger_ = logger.get_logger(__name__)


def send(recipient_email: str, subject: str, message_text: str):
    message = _create_message('me', recipient_email, subject, message_text)
    gmail_service = _build_gmail_service()
    return gmail_service.users().messages().send(userId="me", body=message).execute()


def _create_message(sender: str, to: str, subject: str, message_text: str) -> dict:
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def _build_gmail_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)
