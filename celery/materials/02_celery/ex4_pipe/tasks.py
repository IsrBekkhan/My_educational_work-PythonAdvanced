from celery import Celery

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)


@app.task
def fetch_user_name(id: int) -> str:
    return f'Пётр {id}-й'


@app.task
def greeting_user(name: str) -> str:
    return f'Здравствуй, {name}!'
