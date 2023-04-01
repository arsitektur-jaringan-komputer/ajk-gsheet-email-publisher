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
        self.subject = "Pengumuman Hasil Open Recruitment Admin Lab AJK"


    def set_body(self, recipient):
        body = f"""Hi {recipient['fullname']},
                
Kami ingin memberitahukan bahwa proses Open Recruitment Admin AJK telah selesai dan sayangnya kami harus memberitahu bahwa Anda tidak terpilih sebagai Admin AJK. Kami menghargai waktu dan usaha yang telah Anda berikan selama proses seleksi, dan ingin memberitahu bahwa keputusan ini bersifat mutlak dan hasil pertimbangan dari segala aspek yang telah Anda lakukan selama ini.

Terima kasih atas partisipasi Anda dalam Open Recruitment Admin AJK, dan sukses untuk masa depan Anda. 

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
            message.attach(MIMEText(self.set_body(recipient), "plain"))

            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls(context=context)
                try:
                    server.login(self.main_email, self.password)
                except smtplib.SMTPAuthenticationError:
                    print("Failed to log in to the SMTP server. Please check your email address and password.")
                
                server.sendmail(self.sender_email, recipient['email'], message.as_string())
                print(f"Email sent to {recipient['nickname']} at {recipient['email']}")