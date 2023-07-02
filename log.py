import logging

import ansi.fg


def init_logging():
    logging.basicConfig(level=logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(MyFormatter())
    logging.getLogger().handlers.clear()
    logging.getLogger().addHandler(stream_handler)


class MyFormatter(logging.Formatter):
    default_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: ansi.fg.GREY + "%(asctime)s - (%(filename)s:%(lineno)d): %(message)s" + ansi.fg.RESET,
        logging.INFO: ansi.fg.GREY + "%(message)s" + ansi.fg.RESET,
        logging.WARNING: ansi.fg.YELLOW + default_format + ansi.fg.RESET,
        logging.ERROR: ansi.fg.RED + default_format + ansi.fg.RESET,
        logging.CRITICAL: ansi.fg.BOLD_RED + default_format + ansi.fg.RESET,
    }

    def format(self, record: logging.LogRecord):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
