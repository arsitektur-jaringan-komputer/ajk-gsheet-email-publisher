import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from mailer import Mailer


SERVICE_ACCOUNT_FILE = 'service-account.json'
SPREADSHEET_ID = os.getenv('AJK_SPREADSHEET_PELATIHAN_DOCKER_ID')
PASSWORD = os.getenv('AJK_EMAIL_PASSWORD')

if __name__ == "__main__":
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
    
    service = build('sheets', 'v4', credentials=creds)
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range='sheet1!A:C'
        ).execute()

    header = result['values'][0]
    column_nickname = header.index('Nickname')
    column_email = header.index('Email')
    subject = "Sertifikat Keikutsertaan Pelatihan Docker"
    recipients = []

    values = result.get('values', [])
    for row in values[1:] :
        recipient_nickname = row[column_nickname]
        recipient_email = row[column_email]

        if not recipient_nickname or not recipient_email :
            continue

        recipient = {"name": recipient_nickname, "email": recipient_email}
        recipients.append(recipient)
    
    mailer = Mailer('kamildeka123@gmail.com', PASSWORD, subject)
    mailer.send_emails(recipients)