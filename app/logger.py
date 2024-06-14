import logging


class Logger:
    def __new__(cls):
        logger = logging.getLogger('logging')
        logging.basicConfig(
            filename='logs.txt',
            filemode='a',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level = logging.INFO,
        )
        return logger
