# cat gunicorn_conf.py
import multiprocessing
import os
# See https://docs.gunicorn.org/en/stable/settings.html for details
# note parameters explicitly via gunicorn cmd line overrides what are set here
#  e.g. even though default here is info, "gunicorn --log-level=debug -c [this file]
#       would mean the debug level is debug, not info
import sys

from src.infra.observability.log import EVENT_BUS_LOG_LEVEL, LOG_DATE_FORMAT, LOG_LEVEL, LOG_MESSAGE_FORMAT

environment = os.getenv('ENVIRONMENT')
is_dev = environment == 'dev'

workers_per_core_str = os.getenv("WORKERS_PER_CORE", "2")
web_concurrency_str = os.getenv("WEB_CONCURRENCY", '1')
host = os.getenv("HOST", "0.0.0.0")  # nosec B104
port = os.getenv("PORT", "8000")

accesslog = '-' if is_dev else None

bind_env = os.getenv("BIND", None)
if bind_env:
    use_bind = bind_env
else:
    use_bind = f"{host}:{port}"

cores = multiprocessing.cpu_count()
workers_per_core = float(workers_per_core_str)
default_web_concurrency = workers_per_core * cores
if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    if not web_concurrency > 0:
        raise AssertionError
else:
    web_concurrency = max(int(default_web_concurrency), 2)

# Gunicorn config variables
workers = web_concurrency
worker_class = 'uvicorn.workers.UvicornWorker'
bind = use_bind
keepalive = os.getenv("GUNICORN_KEEPALIVE", 120)
errorlog = "-"
threads = os.getenv("GUNICORN_THREADS", 120)

logconfig_dict = {
    'version': 1,
    'formatters': {
        'generic': {
            'format': LOG_MESSAGE_FORMAT,
            'datefmt': LOG_DATE_FORMAT,
            'class': 'logging.Formatter',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'generic',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'root': {
            'level': LOG_LEVEL,
            'handlers': ['console']
        },
        'gunicorn.error': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
        'event_bus_sdk': {
            'level': EVENT_BUS_LOG_LEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
    },
}


def worker_int(worker) -> None:
    sys.exit(1)


def child_exit(server, worker) -> None:
    sys.exit(1)
