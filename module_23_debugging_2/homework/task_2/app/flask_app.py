import time
import random

from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.route('/is_true/<true_or_false>')
@metrics.counter('calls_count',
                 'amount of function calls',
                 labels={'status_code': lambda resp: resp.status_code})
def first_route(true_or_false: str):
    """
    Это тестовый эндпоинт:
    возвращает ('ok', 200) при запросе http://localhost:5000/is_true/true
    возвращает ('false', 400) при запросе http://localhost:5000/is_true/false

    """
    if true_or_false == 'true':
        time.sleep(random.random() * 0.2)
        return 'ok', 200
    return 'false', 400


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, threaded=True)
