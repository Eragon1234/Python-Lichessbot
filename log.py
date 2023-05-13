import logging


def init_logging():
    logging.basicConfig(level=logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(MyFormatter())
    logging.getLogger().handlers.clear()
    logging.getLogger().addHandler(stream_handler)


class MyFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    default_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + "%(asctime)s - (%(filename)s:%(lineno)d): %(message)s" + reset,
        logging.INFO: grey + "%(message)s" + reset,
        logging.WARNING: yellow + default_format + reset,
        logging.ERROR: red + default_format + reset,
        logging.CRITICAL: bold_red + default_format + reset
    }

    def format(self, record: logging.LogRecord):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
