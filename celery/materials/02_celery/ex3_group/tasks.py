from celery import Celery

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)


@app.task
def buy_milk(volume: int) -> int:
    print(f'Покупаем {volume} литров молока')
    return volume


@app.task
def buy_bread(count: int) -> int:
    print(f'Покупаем {count} буханок хлеба')
    return count
