import logging
import string


class ASCIIFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> int:
        return not any(symb not in string.printable for symb in record.msg)


logging.basicConfig(level="INFO")

logger = logging.getLogger(__name__)
logger.addFilter(ASCIIFilter())


def main():
    logger.info("I should appear")
    logger.info("А я нет")


if __name__ == "__main__":
    main()
