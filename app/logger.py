import logging


class Logger:
    def __new__(cls):
        logger = logging.getLogger('logging')
        logging.basicConfig(
            filename='logging_info.txt',
            filemode='a+',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logger
