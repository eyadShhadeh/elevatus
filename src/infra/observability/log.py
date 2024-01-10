import logging
import os

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev').lower()

LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_MESSAGE_FORMAT = ('%(asctime)s,%(msecs)03d [%(process)s] [%(thread)d] [%(name)s] '
                      '[%(filename)s:%(lineno)d] %(levelname)s %(message)s')


def configure_logging() -> None:  # pragma: no cover
    logging.basicConfig(datefmt=LOG_DATE_FORMAT, format=LOG_MESSAGE_FORMAT, level=LOG_LEVEL)
