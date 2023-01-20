from datetime import date, datetime
from re import match


def format_author(author_str: str) -> str:
    author_str = author_str[0: author_str.rfind(',')]
    author_names = [string for string in author_str.split(', ') if match('[a-zA-Z.-]', string)]
    return ' '.join(reversed(author_names))


def format_due_date(due_date: date) -> str:
    return due_date.strftime('%d/%m/%y')


def parse_date(due_date_string: str) -> date:
    """convert due date string into date type"""
    formatted_string = due_date_string.strip().split(' ')[0]
    try:
        datetime_object = datetime.strptime(formatted_string, '%d/%m/%Y')
    except ValueError:
        datetime_object = datetime.strptime(formatted_string, '%d/%m/%y')
    return datetime_object.date()


class LibraryBook:
    def __init__(self, title: str, author: str, due_date: str, times_renewed: str, check_box):
        self.title = title
        self.author = format_author(author)
        self.due_date = parse_date(due_date)
        self.times_renewed = times_renewed
        self.check_box = check_box

    def is_due(self) -> bool:
        return (self.due_date - date.today()).days <= 0

    def __repr__(self):
        title_str = F'Title -> {self.title}'
        author_str = F'Author -> {self.author}'
        due_date_str = F'Due -> {format_due_date(self.due_date)}'
        return ' | '.join([title_str, author_str, due_date_str])