"""Logging utilities."""
import logging


def create_custom_logger(name):
    """Create a global logger with given name."""
    formatter = logging.Formatter(fmt='[%(asctime)s] %(levelname)s %(name)s:' +
                                      ' %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger
