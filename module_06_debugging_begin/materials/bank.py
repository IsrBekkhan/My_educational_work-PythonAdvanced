import csv
from typing import Optional
import logging

from flask import Flask
from werkzeug.exceptions import InternalServerError


logger = logging.getLogger('invalid_error')

app = Flask(__name__)


@app.route("/bank_api/<branch>/<int:person_id>")
def bank_api(branch: str, person_id: int):
    logger.debug(f'Поиск человека с ID-{person_id} в файле {branch}.txt')
    branch_card_file_name = f"bank_data/{branch}.csv"

    with open(branch_card_file_name, "r", encoding='utf-8') as fi:
        csv_reader = csv.DictReader(fi, delimiter=",")

        for record in csv_reader:
            if int(record["id"]) == person_id:
                return record["name"]
        else:
            return "Person not found", 404


@app.errorhandler(InternalServerError)
def handle_exception(e: InternalServerError):
    original: Optional[Exception] = getattr(e, "original_exception", None)

    if isinstance(original, FileNotFoundError):
        logger.exception(f"Tried to access {original.filename}.", exc_info=original)
    elif isinstance(original, OSError):
        logger.exception(f"Unable to access a card.", exc_info=original)

    logger.exception('Непредвиденная ошибка.', exc_info=original)
    return "Internal server error", 500


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        filename='banking.log',
                        datefmt='%I:%M:%S',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.info('Запуск сервера базы данных банка!')
    app.run()
