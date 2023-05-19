import logging

from ansi import ANSI


def init_logging():
    logging.basicConfig(level=logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(MyFormatter())
    logging.getLogger().handlers.clear()
    logging.getLogger().addHandler(stream_handler)


class MyFormatter(logging.Formatter):
    default_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: ANSI.FG.GREY + "%(asctime)s - (%(filename)s:%(lineno)d): %(message)s" + ANSI.FG.RESET,
        logging.INFO: ANSI.FG.GREY + "%(message)s" + ANSI.FG.RESET,
        logging.WARNING: ANSI.FG.YELLOW + default_format + ANSI.FG.RESET,
        logging.ERROR: ANSI.FG.RED + default_format + ANSI.FG.RESET,
        logging.CRITICAL: ANSI.FG.BOLD_RED + default_format + ANSI.FG.RESET,
    }

    def format(self, record: logging.LogRecord):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
