import sys
from logging import config, getLogger, basicConfig, StreamHandler, Formatter
from logging_tree import format

from logging_config import MyFileHandler, config_dict
from utils import string_to_operator


def logger_maker():
    # stream_handler = StreamHandler(stream=sys.stdout)
    # file_handler = MyFileHandler('logger.log')
    # formatter = Formatter('%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s')
    # stream_handler.setFormatter(formatter)
    # file_handler.setFormatter(formatter)
    #
    # basicConfig(level='DEBUG', handlers=[stream_handler, file_handler])

    config.dictConfig(config_dict)


logger_maker()
app_logger = getLogger('app_logger')

with open('logging_tree.txt', 'w') as log_file:
    log_file.write(format.build_description())


def calc(args):
    app_logger.debug(f'Arguments: {args}')

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        app_logger.exception("Error while converting number 1", exc_info=e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        app_logger.exception("Error while converting number 1", exc_info=e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    app_logger.info(f"Result: {result}")
    app_logger.info(f"{num_1} {operator} {num_2} = {result}")


if __name__ == '__main__':
    # calc(sys.argv[1:])
    calc(('53', '+', '5'))
