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

    recipients = []
    for row in rows:
        name = row["Name"]
        if name:
            recipient = Recipient(name, row["Email"])
            recipients.append(recipient) # maybe wrong

    sender_email = 'xxx@gmail.com'
    sender_password = os.getenv('EMAIL_PASSWORD') # adjust it !

    email_subject = 'TULIS SUBJECT DISINI'
    body = f"""
Dear {recipient},
        
Kami ingin mengucapkan terima kasih kepada Anda atas partisipasi dalam pelatihan Docker yang telah diselenggarakan oleh Lab AJK. Kami berharap bahwa pelatihan ini memberikan manfaat yang besar bagi Anda dan membantu meningkatkan keterampilan Anda dalam menggunakan teknologi Docker.

Dalam rangka mengapresiasi partisipasi Anda, kami ingin memberikan sertifikat keikutsertaan dalam pelatihan Docker ini. 

Kami berharap dapat berkolaborasi dengan Anda lagi di masa depan dan terus mendukung pengembangan keterampilan dan pengetahuan teknologi Anda.

Salam hangat,
AJK
"""

    """
    TODO :
    1. Recipient harusnya dictionary array
    2. body karena tergantung sama recipient harus di dalam looping
    """
    # for recipient in recipients :
        # mailer = Mailer(sender_email, recipient)