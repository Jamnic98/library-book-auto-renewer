from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date


class MimeEmail:
    def __init__(self, subject, receiver, sender, send_date=date.today()):
        self.message = MIMEMultipart()
        self.message['Subject'] = subject
        self.message['To'] = receiver
        self.message['From'] = sender
        date_string = f'{send_date.day}/{send_date.month}/{send_date.year}'
        self.message['Date'] = date_string

    def add_plain_text_message(self, text_content):
        self.message.attach(MIMEText(text_content, 'plain'))

    def add_html_message(self, html_content):
        self.message.attach(MIMEText(html_content, 'html'))


def create_list_item(data):
    return wrap_element("li", data)


def create_list(books):
    list_items = ''.join([create_list_item(book.title) for book in books])
    return wrap_element('ul', list_items)


def wrap_element(tag_name, data, style=''):
    return f'<{tag_name} {style}>{data}</{tag_name}>'


def generate_html_message(message, books):
    return f'<html><body>' \
           f'<p>{message}</p><br/>' \
           f'{create_list(books)}' \
           f'</body></html> '
