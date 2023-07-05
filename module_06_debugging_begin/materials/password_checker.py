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

    result = password_safety_checker(password)

    if result:
        recommendations = ', '.join(result)
        logger.warning(f'Вы ввели небезопасный пароль: {recommendations}.')

    try:
        hasher = hashlib.md5()
        logger.debug(f'Мы создали объект hasher {hasher}')

        hasher.update(password.encode("utf-8"))
        logger.debug(f'Захэширован введенный пароль: {hasher.hexdigest()}')

        if hasher.hexdigest() == "098f6bcd4621d373cade4e832627b4f6":
            logger.info("Пароль верный!")
            return True
    except ValueError as ex:
        logger.exception("Вы ввели некорректный символ ", exc_info=ex)

    return False


def password_safety_checker(password: str) -> list:
    symbols = '!@#$%^&*()-+=_'
    isupper = False
    islower = False
    isdigit = False
    is_more_symbols = False
    is_special_symbol = False
    messages = list()

    if len(password) >= 8:
        is_more_symbols = True

    for symbol in password:

        if symbol.isupper():
            isupper = True

        if symbol.islower():
            islower = True

        if symbol.isdigit():
            isdigit = True

        if symbol in symbols:
            is_special_symbol = True

    if not isupper:
        messages.append('нет хотя бы одной заглавной буквы')

    if not islower:
        messages.append('нет хотя бы одной строчной буквы')

    if not isdigit:
        messages.append('нет хотя бы одной цифры')

    if not is_more_symbols:
        messages.append('в пароле менее 8 символов')

    if not is_special_symbol:
        messages.append('нет хотя бы одного специального сивола (!@#$%^&*()-+=_)')

    return messages


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Вы пытаетесь аутентифицироваться в Skillbox")

    while True:
        try:
            count_number: int = int(input("Сколько неверных попыток ввода вам требуется? "))

            if count_number < 2 or count_number > 10:
                raise ValueError

            break
        except ValueError:
            logger.warning('Пожалуйста введите числовое значение диапазона 2-10')

    logger.info(f"У вас есть {count_number} попыток")

    while count_number > 0:
        if input_and_check_password():
            exit(0)
        count_number -= 1

    logger.error("Пользователь трижды ввёл не правильный пароль!")
    exit(1)
