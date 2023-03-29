import os
import re
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mailer:
    def __init__(self, sender_email, password, receipent_email, subject, body, smtp_server="smpt.gmail.com", port=587):
        self.sender_email = sender_email
        self.password = password
        self.receipent_email = receipent_email
        self.subject = subject
        self.body = body
        self.smtp_server = smtp_server
        self.port = port
        self.context = ssl.create_default_context()
        self.recipients = []

    def send_emails(self):
        for recipient in self.recipients:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = self.receipent_email
            message["Subject"] = self.subject
            message.attach(MIMEText(self.body, "plain"))

            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls(context=self.context)
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, recipient.email, message.as_string())
                print(f"Email sent to {recipient.name} at {recipient.email}")