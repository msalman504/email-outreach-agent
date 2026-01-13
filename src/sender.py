import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time

class HostingerSender:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.hostinger.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 465))
        self.email_address = os.getenv("EMAIL_ADDRESS")
        self.password = os.getenv("EMAIL_PASSWORD")
        
        if not self.email_address or not self.password:
            raise ValueError("EMAIL_ADDRESS or EMAIL_PASSWORD not set in environment.")

    def send_email(self, to_email, subject, body, attachment_path=None):
        """Sends an email via Hostinger SMTP with optional attachment."""
        message = MIMEMultipart()
        message["From"] = self.email_address
        message["To"] = to_email
        message["Subject"] = subject

        # Convert Markdown to HTML for basic formatting
        import re
        html_body = body.replace("\n", "<br>")
        html_body = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html_body) # Bold
        
        # Attach both Plain and HTML versions (Multipart/Alternative)
        # Actually, user just wants "Formatted". HTML-only is riskier for spam filters but simpler.
        # Let's do HTML.
        message.attach(MIMEText(html_body, "html"))

        if attachment_path and os.path.exists(attachment_path):
            from email.mime.base import MIMEBase
            from email import encoders
            
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(attachment_path)}",
            )
            message.attach(part)

        context = ssl.create_default_context()
        
        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                server.login(self.email_address, self.password)
                server.sendmail(self.email_address, to_email, message.as_string())
            print(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email to {to_email}: {e}")
            return False

def send_bulk_emails(email_list, delay=2):
    """
    Sends emails to a list with a delay to avoid rate limits.
    email_list: List of dicts with 'to', 'subject', 'body'
    """
    sender = HostingerSender()
    for item in email_list:
        sender.send_email(item['to'], item['subject'], item['body'])
        time.sleep(delay)
