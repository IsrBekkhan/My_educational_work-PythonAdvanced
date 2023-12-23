from typing import Tuple
from flask import Flask, Response, jsonify, request
import sentry_sdk

app = Flask(__name__)

# sentry self-host init
# sentry_sdk.init(
#     dsn="http://fb6300afcc47a59a8b8e25a9ef908335@127.0.0.1:9000/2",
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     traces_sample_rate=1.0,
# )

# sentry.io init
sentry_sdk.init(
    dsn="https://bb9e1a6250f6fff04820703e9beee3bb@o4506360207966208.ingest.sentry.io/4506393743720448",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


@app.route('/hello', methods=['GET'])
def hello_world() -> Tuple[Response, int]:
    for_raise = 1 / 0  # raises an error
    return jsonify({'message': 'Hello World!'}), 200


@app.route('/test_type')
def test_type():
    user_id = request.args.get('user_id')
    user_id = float(user_id)


@app.route('/test')
def ll():
    raise IndexError


if __name__ == '__main__':
    app.run()

