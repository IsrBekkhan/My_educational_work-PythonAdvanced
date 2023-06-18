"""
Количество попыток ввода неправильного пароля у нас строго зашито в коде программы, это плохо.
Пусть наша программа будет чуть более вежливой и спросит, сколько раз пользователь хочет ввести пароль.

Минимальное количество раз — два, максимальное — десять.

В случае возникновения ошибок нужно, конечно, правильным образом их залогировать.

В качестве кода программы можете взять то, что у вас получилось в результате
работы над work_3_1.py или нижеследующий код
"""

import getpass
import hashlib
import logging

logger = logging.getLogger("password_checker")


def input_and_check_password():
    logger.debug("Начало input_and_check_password")
    password: str = getpass.getpass()

    if not password:
        logger.warning("Вы ввели пустой пароль.")
        return False

    try:
        hasher = hashlib.md5()

        hasher.update(password.encode("latin-1"))

        if hasher.hexdigest() == "098f6bcd4621d373cade4e832627b4f6":
            return True
    except ValueError as ex:
        logger.exception("Вы ввели некорректный символ ", exc_info=ex)

    return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Вы пытаетесь аутентифицироваться в Skillbox")
    count_number: int = 3
    logger.info(f"У вас есть {count_number} попыток")

    while count_number > 0:
        if input_and_check_password():
            exit(0)
        count_number -= 1

    logger.error("Пользователь трижды ввёл не правильный пароль!")
    exit(1)
