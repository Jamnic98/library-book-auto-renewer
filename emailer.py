from os import getenv
import smtplib
import ssl


class Emailer:
    def __init__(self, smtp_server, port=587):
        self.port = port
        self.sender_email = getenv('SENDER_ADDRESS')
        self.sender_password = getenv('SENDER_PASSWORD')
        # SMTP
        self.server = smtplib.SMTP(smtp_server, port)
        self.server.starttls(context=ssl.create_default_context())
        self.server.login(self.sender_email, self.sender_password)

    def send_email(self, receiver_email, message):
        self.server.sendmail(self.sender_email, receiver_email, message)
