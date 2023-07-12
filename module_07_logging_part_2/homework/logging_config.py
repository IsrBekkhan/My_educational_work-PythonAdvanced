import sys
from custom_handlers import MyFileHandler, MyFilter
from logging.handlers import TimedRotatingFileHandler, HTTPHandler


config_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base': {
            'format': '%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'base',
            'stream': sys.stdout
        },
        'file': {
            '()': MyFileHandler,
            'level': 'DEBUG',
            'filename': 'logger.log',
            'formatter': 'base'
        },
        'rotate_file': {
            '()': TimedRotatingFileHandler,
            'level': 'INFO',
            'filename': 'rotate_logger.log',
            'when': 'H',
            'interval': 10,
            'backupCount': 1,
            'formatter': 'base'
        },
        'http': {
            '()': HTTPHandler,
            'host': '127.0.0.1:5000',
            'url': '/log',
            'method': 'POST',
            'level': 'DEBUG'
        }
    },
    'loggers': {
        'app_logger': {
            'level': 'DEBUG',
            'handlers': ['file']
        },
        'utils_logger': {
            'level': 'DEBUG',
            'handlers': ['rotate_file'],
            'filters': ['is_ascii']
        }
    },
    'filters': {
        'is_ascii': {
            '()': MyFilter
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'http'],
        'propagate': False
    }
}
