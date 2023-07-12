import logging
import sys
from logging import LogRecord


class MyStreamHandler(logging.Handler):

    def __init__(self, thread=sys.stderr) -> None:
        super().__init__()
        self.thread = thread

    def emit(self, record: LogRecord) -> None:
        print('<' * 40)
        for key, value in vars(record).items():
            print(key, '-', value)
        print('>' * 40)
        message = self.format(record)
        self.thread.write(message)


dict_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base': {
            'format': '%(name)s || %(levelname)s || %(message)s || %(module)s.%(funcName)s:%(lineno)d || %(very)s'
        }
    },
    'handlers': {
        'console': {
            '()': MyStreamHandler,
            'level': 'DEBUG',
            'formatter': 'base',
            'thread': sys.stdout
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'base',
            'filename': 'log_file.log',
            'mode': 'a',
            'encoding': 'utf-8'

        }
    },
    'loggers': {
        'sub_1': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        },
        'sub_2': {
            'handlers': ['file'],
            'propagate': False
        },
        'sub_1.sub_sub_1': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    }
}
