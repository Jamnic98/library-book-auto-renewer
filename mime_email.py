from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MimeEmail:
    def __init__(self, subject, receiver, sender, send_date=date.today()):
        self.message = MIMEMultipart()
        self.message['Subject'] = subject
        self.message['To'] = receiver
        self.message['From'] = sender
        self.message['Date'] = send_date

    def add_plain_text_message(self, text_content):
        self.message.attach(MIMEText(text_content, 'plain'))

    def add_html_message(self, html_content):
        self.message.attach(MIMEText(html_content, 'plain'))
