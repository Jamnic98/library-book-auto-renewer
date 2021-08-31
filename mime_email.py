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


def create_table_rows(books):
    return ''.join(create_table_row(book) for book in books)


def create_table_row(book):
    style = 'border: 1px solid black; padding: 2px'
    data = [book.title, book.author, book.due_date, book.times_renewed]
    table_data = ''.join([wrap_element("td", data_point, style) for data_point in data])
    return wrap_element("tr", table_data, style)


def create_table_header(data, style):
    header_data = ''.join([wrap_element("th", data_point) for data_point in data])
    return wrap_element("tr", header_data, style)


def wrap_element(tag_name, data, style=''):
    return f'<{tag_name} {style}>{data}</{tag_name}>'


def generate_html_message(message, books):
    style = 'border: 1px solid black; padding: 2px'
    column_titles = ['Title', 'Author', 'Due Date', 'Times Renewed']
    table_header = create_table_header(column_titles, style)
    table_rows = create_table_rows(books)
    table = wrap_element("table", f'{table_header}{table_rows}', style)

    return f'<html><body>' \
           f'<p>{message}</p><br/>' \
           f'{table}' \
           f'</body></html> '
