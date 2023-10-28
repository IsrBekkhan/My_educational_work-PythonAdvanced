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
    sender.add_periodic_task(5.0, check_cat.s())
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        check_cat.s()
    )


@app.task
def check_cat():
    if random() < 0.5:
        print("Кот ничего не сломал.")
    else:
        print("Кот что-то сломал...")
