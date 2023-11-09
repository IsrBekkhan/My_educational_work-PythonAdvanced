from random import random

from celery import Celery
from celery.schedules import crontab

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(2, check_cat.s())
    sender.add_periodic_task(
        crontab(hour=12, minute=4),
        check_cat.s()
    )


@app.task
def check_cat():
    if random() < 0.5:
        print("Кот ничего не сломал.")
    else:
        print("Кот что-то сломал...")
