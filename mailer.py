import io
import smtplib, ssl
import concurrent.futures
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LEDGER


class Mailer:
    def __init__(self, main_email, password, sender_email, smtp_server='smtp.office365.com', port=587):
        self.main_email = main_email
        self.password = password
        self.sender_email = sender_email
        self.smtp_server = smtp_server
        self.port = port
        self.subject = "subject here"


    def set_body(self, recipient):
        body = f"""
body here (HTML format)
"""
        return MIMEText(body, 'html')


    def generate_certificate_pdf(self, recipient):
        templated_certificate = f"template_certificate.pdf"
        edited_certificate_file = f"output/{recipient['nrp']}_{recipient['fullname']}_certificate.pdf"

        existing_pdf = PdfReader(open(templated_certificate, "rb"))
        width = existing_pdf.pages[0].mediabox.width
        
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=LEDGER)
        can.setFillColorRGB(0, 0, 0)
        can.setFont("Times-Roman", 32)
        can.drawCentredString(width/2, 412, f"{recipient['fullname']}")
        can.save()

        packet.seek(0)
        new_pdf = PdfReader(packet)

        output = PdfWriter()

        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)

        outputStream = open(edited_certificate_file, "wb")
        output.write(outputStream)
        outputStream.close()

        return edited_certificate_file


    def send_email(self, context, recipient):
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = recipient['email']
        message["Subject"] = self.subject
        message.attach(self.set_body(recipient))
            
        certificate_file = self.generate_certificate_pdf(recipient)
        if certificate_file.endswith('.pdf'):
            with open(certificate_file, "rb") as f:
                attach = MIMEApplication(f.read(),_subtype="pdf")
            attach.add_header('Content-Disposition','attachment',filename=str(f"Sertifikat_{recipient['nrp']}_{recipient['fullname']}.pdf"))
            message.attach(attach)
        else:
            print(f"Certificate file {certificate_file} has unsupported format. Skipping attachment.")

        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls(context=context)
            try:
                server.login(self.main_email, self.password)
            except smtplib.SMTPAuthenticationError:
                return("Failed to log in to the SMTP server. Please check your email address and password.")
            
            try:
                server.sendmail(self.sender_email, recipient['email'], message.as_string())
                return f"[SUCCEED] Email sent to {recipient['fullname'].upper()} at {recipient['email']}"
            except smtplib.SMTPRecipientsRefused:
                return f"[FAILED] Email sent to {recipient['fullname'].upper()} at {recipient['email']}"


    def send_email_concurrently(self, recipients):
        context = ssl.create_default_context()

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor, open('output.txt', 'w') as fp:
            futures = []
            for recipient in recipients:
                futures.append(executor.submit(self.send_email, context, recipient))

            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    fp.write(result + '\n')
                    fp.flush()
                except Exception as e:
                    fp.write(f"An error occurred: {e}\n")
                    fp.flush()