import gspread, os
from google.oauth2.service_account import Credentials
from receipent import Recipient
from mailer import Mailer


SERVICE_ACOUNT = ''
SHEET_NAME = ''

if __name__ == "__main__":
    credentials = Credentials.from_service_account_file(SERVICE_ACOUNT)
    client = gspread.authorize(credentials)

    sheet = client.open(SHEET_NAME).sheet1

    rows = sheet.get_all_records()

    recipients = {}
    for row in rows:
        name = row["Name"]
        if name:
            recipient = Recipient(name, row["Email"])
            recipients[recipient.name].append(recipient.email)

    sender_email = 'xxx@gmail.com'
    sender_password = os.getenv('EMAIL_PASSWORD')
    email_subject = 'TULIS SUBJECT DISINI'
    
    for recipient_name, recipient_email in recipients.items() :
        body = f"""
Dear {recipient_name},
        
Kami ingin mengucapkan terima kasih kepada Anda atas partisipasi dalam pelatihan Docker yang telah diselenggarakan oleh Lab AJK. Kami berharap bahwa pelatihan ini memberikan manfaat yang besar bagi Anda dan membantu meningkatkan keterampilan Anda dalam menggunakan teknologi Docker.

Dalam rangka mengapresiasi partisipasi Anda, kami ingin memberikan sertifikat keikutsertaan dalam pelatihan Docker ini. 

Salam hangat,
AJK
"""

        mailer = Mailer(sender_email, password, recipient_email, email_subject, body)
        mailer.send_emails()