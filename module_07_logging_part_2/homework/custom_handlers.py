from logging import Handler, LogRecord, Filter


class MyFilter(Filter):

    def filter(self, record: LogRecord) -> bool:
        return record.msg.isascii()


class MyFileHandler(Handler):

    def __init__(self, filename: str, mode: str = 'a'):
        super().__init__()
        self.file_name = filename
        self.mode = mode

    def emit(self, record: LogRecord) -> None:
        full_file_name = '_'.join((record.levelname, self.file_name))
        message = self.format(record)

        with open(full_file_name, mode=self.mode, encoding='utf-8') as log_file:
            log_file.write(message + '\n')
