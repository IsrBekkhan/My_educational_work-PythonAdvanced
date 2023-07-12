import logging
import logging.config

from last_task import dict_config


logging.config.dictConfig(dict_config)

root_logger = logging.getLogger()
sub_logger_1 = logging.getLogger('sub_1')
sub_logger_1.propagate = False
sub_logger_2 = logging.getLogger('sub_2')
sub_sub_logger_1 = logging.getLogger('sub_1.sub_sub_1')


def main():
    sub_logger_1.info('Тест sub_logger_1', extra={'very': 'much'})


if __name__ == '__main__':
    main()
