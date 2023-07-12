from flask import Flask, request
from logging import Formatter, makeLogRecord
from typing import Tuple


formatter = Formatter(fmt='%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s')

app = Flask(__name__)


@app.route('/log', methods=['POST', 'GET'])
def log() -> Tuple[str, int]:

    if request.method == 'GET':
        log_data = request.args.to_dict()

    if request.method == 'POST':
        log_data = request.form.to_dict()

    log_record = makeLogRecord(log_data)
    log_message = formatter.formatMessage(log_record)
    print(log_message)

    return 'OK', 200


if __name__ == '__main__':
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
