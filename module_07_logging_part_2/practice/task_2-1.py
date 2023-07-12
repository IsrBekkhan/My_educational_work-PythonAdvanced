import logging
from logging.handlers import HTTPHandler


http_handler = HTTPHandler(host='http://127.0.0.1:5000', url='/log', method='POST')


formatter = logging.Formatter(
    fmt='%(name)s || %(levelname)s || %(message)s || %(module)s.%(funcName)s:%(lineno)d')

root_handler = logging.StreamHandler()
root_handler.setLevel('DEBUG')
root_handler.setFormatter(formatter)

root_logger = logging.getLogger()
root_logger.addHandler(http_handler)
root_logger.setLevel('INFO')

custom_handler = logging.StreamHandler()
custom_handler.setLevel('DEBUG')

custom_handler.setFormatter(formatter)

sub_logger_1 = logging.getLogger('sub_1')
sub_logger_1.addHandler(custom_handler)

sub_logger_2 = logging.getLogger('sub_2')
sub_logger_2.propagate = False

sub_sub_logger_1 = logging.getLogger('sub_1.sub_sub_1')
sub_sub_logger_1.setLevel('DEBUG')
sub_sub_logger_1.addHandler(custom_handler)
sub_sub_logger_1.propagate = False


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
