dict_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base': {
            'format': '%(name)s || %(levelname)s || %(message)s || %(module)s.%(funcName)s:%(lineno)d'
        }
    },
    'loggers': {
        'sub_1': {
            'level': 'INFO'
        },
        'sub_2': {},
        'sub_1.sub_sub_1': {
            'level': 'DEBUG'
        }
    },
    'root': {
        'level': 'DEBUG'
    }
}