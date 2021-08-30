import smtplib
from emailer import Emailer


with smtplib.SMTP('localhost', 1025) as server:
    server.sendmail('test.email@gmail.com', 'test.email@gmail.com', 'hello')
