"""
Email Sender Module

Handles email sending functionality for news digests.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender:
    """Handle email sending functionality"""
    
    def __init__(self, smtp_server: str, smtp_port: int, email: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
    
    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send email with news digest"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            text = msg.as_string()
            server.sendmail(self.email, to_email, text)
            server.quit()
            
            print(f"Email sent successfully to {to_email}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"Email authentication failed: {e}")
            print("\n🔒 Gmail Authentication Help:")
            print("1. Make sure you're using an App Password, not your regular Gmail password")
            print("2. Enable 2-Factor Authentication on your Google account")
            print("3. Generate an App Password: https://myaccount.google.com/apppasswords")
            print("4. Use the 16-character app password (no spaces) as EMAIL_PASSWORD")
            print("5. Make sure 'Less secure app access' is enabled if not using 2FA")
            return False
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False 