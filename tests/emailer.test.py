import smtplib
from datetime import date
from library_book import LibraryBook
from mime_email import MimeEmail, generate_html_message

books = [LibraryBook('title', 'author', '1/31/1998', '5', None)]

email = MimeEmail('Test', 'test@test.com', 'test0@test.com', '31/08/2021')
email.add_html_message(generate_html_message('some text', books))

with smtplib.SMTP('localhost', 1025) as server:
    server.sendmail('test.email@gmail.com', 'test.email@gmail.com', email.message.as_string())
