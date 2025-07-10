import os
import json
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()


def acessando_drive():
    load_dotenv()
    info = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
    cred_dict = json.loads(info)
    SCOPES = os.getenv('SCOPES_DRIVE').split(',')
    creds = service_account.Credentials.from_service_account_info(
        cred_dict, scopes=SCOPES)
    drive_service = build("drive", "v3", credentials=creds)
    return drive_service
