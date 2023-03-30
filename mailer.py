import os
import re
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mailer:
    def __init__(self, sender_email, password, recipient_email, recipient_nickname, subject, smtp_server="smpt.gmail.com", port=587):
        self.sender_email = sender_email
        self.password = password
        self.receipent_email = recipient_email
        self.recipient_nickname = recipient_nickname
        self.subject = subject
        self.smtp_server = smtp_server
        self.port = port
        self.context = ssl.create_default_context()
        self.recipients = []

    def set_body(self):
        body = f"""
Dear {self.recipient_nickname},
                
Kami ingin mengucapkan terima kasih kepada Anda atas partisipasi dalam pelatihan Docker yang telah diselenggarakan oleh Lab AJK. Kami berharap bahwa pelatihan ini memberikan manfaat yang besar bagi Anda dan membantu meningkatkan keterampilan Anda dalam menggunakan teknologi Docker.

Dalam rangka mengapresiasi partisipasi Anda, kami ingin memberikan sertifikat keikutsertaan dalam pelatihan Docker ini. 

Salam hangat,
AJK
"""
        return body

    def send_emails(self):
        for recipient in self.recipients:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = self.recipient_email
            message["Subject"] = self.subject
            message.attach(MIMEText(self.set_body(), "plain"))

            print(recipient)
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls(context=self.context)
                try:
                    server.login(self.sender_email, self.password)
                except smtplib.SMTPAuthenticationError:
                    print("Failed to log in to the SMTP server. Please check your email address and password.")
                
                server.sendmail(self.sender_email, recipient.email, message.as_string())
                print(f"Email sent to {recipient.name} at {recipient.email}")