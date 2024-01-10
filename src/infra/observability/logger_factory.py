import logging
import os
import sys

from loguru import logger

LOG_LEVEL = os.getenv('LOG_LEVEL', 'info')
EVENT_BUS_LOG_LEVEL = os.getenv('EVENT_BUS_LOG_LEVEL', LOG_LEVEL)

LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


LOG_MESSAGE_FORMAT = "<level>{level: <8}</level> - <cyan>{extra[source]}</cyan>:<cyan>{extra[funcName]}</cyan> - \
<level>{extra[stack_info]}</level> - <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> - <level>{message}</level>"


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record):  # type:ignore
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        log = logger.bind(funcName=record.funcName, source=record.name, stack_info=record.filename)
        log.opt(
            depth=depth,
            exception=record.exc_info
        ).log(level, record.getMessage())


class CustomizeLogger:

    @classmethod
    def make_logger(cls):  # type:ignore

        logger = cls.customize_logging(
            level=LOG_LEVEL,
            format=LOG_MESSAGE_FORMAT
        )
        return logger

    @classmethod
    def customize_logging(cls,  # type:ignore
                          level: str,
                          format: str
                          ):

        logger.remove()
        logger.add(sys.stdout,
                   enqueue=True,
                   backtrace=True,
                   colorize=True,
                   level=level.upper(),
                   format=format
                   )
        logging.basicConfig(handlers=[InterceptHandler()], level=0)

        logging.getLogger("gunicorn.access").handlers = [InterceptHandler()]
        for _log in ['uvicorn',
                     'fastapi',
                     'datadog',
                     'worker',
                     'uvicorn.access',
                     'uvicorn.error',
                     'gunicorn',
                     'gunicorn.error',
                     'src',
                     '__main__',
                     'ddtrace',
                     'event_bus_sdk',
                     'botocore',
                     'resin_shared_library',
                     'boto3']:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)


log = CustomizeLogger.make_logger()
