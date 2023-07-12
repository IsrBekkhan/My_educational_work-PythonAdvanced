import logging
import logging.config

# from dict_config import dict_config
from last_task import dict_config


logging.config.dictConfig(dict_config)

root_logger = logging.getLogger()
sub_logger_1 = logging.getLogger('sub_1')
sub_logger_2 = logging.getLogger('sub_2')
sub_sub_logger_1 = logging.getLogger('sub_1.sub_sub_1')


def main():
    print(root_logger)
    print(root_logger.handlers)
    root_logger.debug('Тест root_logger')
    print()
    print(sub_logger_1)
    print(sub_logger_1.handlers)
    sub_logger_1.info('Тест sub_logger_1')
    print()
    print(sub_logger_2)
    print(sub_logger_2.handlers)
    sub_logger_2.info('Тест sub_logger_2')
    print()
    print(sub_sub_logger_1)
    print(sub_sub_logger_1.handlers)
    sub_sub_logger_1.debug('Тест sub_sub_logger_1')


if __name__ == '__main__':
    main()
