dict_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base': {
            'format': '%(name)s || %(levelname)s || %(message)s || %(module)s.%(funcName)s:%(lineno)d'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'base'
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
