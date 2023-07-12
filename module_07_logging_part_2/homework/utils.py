from typing import Union, Callable
from operator import sub, mul, truediv, add

from logging import getLogger


utils_logger = getLogger('utils_logger')

OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}

Numeric = Union[int, float]


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    utils_logger.debug(f'Запуск функции {string_to_operator.__name__} с аргументом {value}')
    if not isinstance(value, str):
        utils_logger.error(f"wrong operator type '{value}'")
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        utils_logger.error(f"wrong operator value '{value}'")
        raise ValueError("wrong operator value")

    return OPERATORS[value]
