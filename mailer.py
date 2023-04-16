import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from PIL import Image, ImageDraw, ImageFont

class Mailer:
    def __init__(self, main_email, password, sender_email, smtp_server='smtp.office365.com', port=587):
        self.main_email = main_email
        self.password = password
        self.sender_email = sender_email
        self.smtp_server = smtp_server
        self.port = port
        self.subject = "FILL THE EMAIL SUBJECT HERE"


    def set_body(self, recipient):
        body = f"""Hi {recipient['fullname']},
FILL THE BODY HERE
"""
        return body


    def generate_certificate(self, recipient):
        img = Image.open('template_sertifikat.png')
        draw = ImageDraw.Draw(img)

        ## For recipient name
        font = ImageFont.truetype("Inter-Bold.ttf", 60) 
        text = f"{recipient['fullname'].upper()}"

        img_width, img_height = img.size
        text_width, text_height = draw.textsize(text, font)

        x = (img_width - text_width) / 2
        draw.text((x,330), text, fill="black", font=font)

        ## Saving the output
        edited_certificate_file = f"output/{recipient['nrp']}_{recipient['fullname']}_certificate.png"
        img.save(edited_certificate_file, "PNG")

        return edited_certificate_file


    def send_emails(self, recipients):
        context = ssl.create_default_context()

        for recipient in recipients:
            
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = recipient['email']
            message["Subject"] = self.subject
            message.attach(MIMEText(self.set_body(recipient), "plain"))

            with open(self.generate_certificate(recipient), 'rb') as file:
                img_data = file.read()
            image = MIMEImage(img_data)
            image.add_header('Content-Disposition', 'attachment', filename='certificate.png')
            message.attach(image)

            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls(context=context)
                try:
                    server.login(self.main_email, self.password)
                except smtplib.SMTPAuthenticationError:
                    print("Failed to log in to the SMTP server. Please check your email address and password.")
                
                server.sendmail(self.sender_email, recipient['email'], message.as_string())
                print(f"Email sent to {recipient['nickname']} at {recipient['email']}")