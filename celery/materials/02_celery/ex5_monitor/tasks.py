import time

from celery import Celery

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)


@app.task
def heavy_task(n: int) -> int:
    result = 1
    for i in range(2, n):
        result *= i
        time.sleep(0.01)
    return result
