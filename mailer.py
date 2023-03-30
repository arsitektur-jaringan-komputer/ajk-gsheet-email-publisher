import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mailer:
    def __init__(self, main_email, password, sender_email, smtp_server='smtp.office365.com', port=587):
        self.main_email = main_email
        self.password = password
        self.sender_email = sender_email
        self.smtp_server = smtp_server
        self.port = port
        self.subject = "[TESTING TOOLS] Sertifikat Keikutsertaan Pelatihan Docker"

    def set_body(self, recipient):
        body = f"""Dear {recipient},
                
Kami ingin mengucapkan terima kasih kepada Anda atas partisipasi dalam pelatihan Docker yang telah diselenggarakan oleh Lab AJK. Kami berharap bahwa pelatihan ini memberikan manfaat yang besar bagi Anda dan membantu meningkatkan keterampilan Anda dalam menggunakan teknologi Docker.

Dalam rangka mengapresiasi partisipasi Anda, kami ingin memberikan sertifikat keikutsertaan dalam pelatihan Docker ini. 

Salam hangat,
AJK
"""
        return body

    def send_emails(self, recipients):
        context = ssl.create_default_context()

        for recipient in recipients:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = recipient['email']
            message["Subject"] = self.subject
            message.attach(MIMEText(self.set_body(recipient['name']), "plain"))

            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls(context=context)
                try:
                    server.login(self.main_email, self.password)
                except smtplib.SMTPAuthenticationError:
                    print("Failed to log in to the SMTP server. Please check your email address and password.")
                
                server.sendmail(self.sender_email, recipient['email'], message.as_string())
                print(f"Email sent to {recipient['name']} at {recipient['email']}")