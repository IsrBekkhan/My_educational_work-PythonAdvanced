from celery import Celery
from celery.result import AsyncResult
from celery.local import PromiseProxy

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)


@app.task
def add(x, y):
    return x + y


# add: PromiseProxy
#
# result: AsyncResult = add.delay(2, 5)
# print(result.__repr__())
#
# print(result.get())