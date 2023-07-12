import logging
import unicodedata


class ReplaceASCIIFilter(logging.Filter):
    @staticmethod
    def _normalize_char(char):
        try:
            cname = unicodedata.name(char)
            cname = cname[: cname.index(" WITH")]
            return unicodedata.lookup(cname)
        except (ValueError, KeyError):
            return char

    def filter(self, record: logging.LogRecord) -> int:
        record.msg = "".join(self._normalize_char(c) for c in record.msg)
        return 1


logging.basicConfig(level="INFO")

logger = logging.getLogger(__name__)
logger.addFilter(ReplaceASCIIFilter())


def main():
    # print(unicodedata.name("ö"))
    logger.info("Die Königin der Nacht blüht nachts")


if __name__ == "__main__":
    main()
