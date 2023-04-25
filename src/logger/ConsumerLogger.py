import logging

LOGGER_LEVEL = logging.DEBUG
FORMATTER = "%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s"


class ConsumerLogger:
    _logger = None

    def __new__(cls, *args, **kwargs):
        if cls._logger is None:
            cls._logger = super().__new__(cls, *args, **kwargs)
            cls._logger = logging.getLogger()
            cls._logger.setLevel(LOGGER_LEVEL)
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(FORMATTER))
            cls._logger.addHandler(handler)
        return cls._logger
