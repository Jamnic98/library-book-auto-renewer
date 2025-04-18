import logging
from app.utlis.settings import config


class Logger:
    def __new__(cls):
        log = logging.getLogger('logging')
        log.setLevel(logging.INFO)
        # create a formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # Create a file handler
        file_handler = logging.FileHandler('logs.txt')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)

        if config["ENV"] != 'production':
            # Create a stream handler for console output
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            log.addHandler(console_handler)
        return log


logger = Logger()
