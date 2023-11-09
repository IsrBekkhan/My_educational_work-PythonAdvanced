"""
Celery-задачи
"""
from celery import Celery, group
from celery.schedules import crontab
from shutil import rmtree

from image import blur_image
from mail import send_email, send_newsletter
from database import Subscription, Task
from PIL.Image import Image

celery_app = Celery(
    'celery_',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)


@celery_app.task
def process_images(src_filename: str, dst_filename: str, task_id: str, email: str):
    """
    Функция, которая применяет эффект размытия к файлу изображения,
    отправляет его на указанную почту и удаляет временные файлы
    после отправки всех фото.
    """
    blur_image(src_filename, dst_filename)
    Task.update_progress(task_id)

    send_email(order_id=task_id, receiver=email, filename=dst_filename)
    if Task.is_done(task_id):
        rmtree(task_id, ignore_errors=True)
        rmtree(f'blur_{task_id}', ignore_errors=True)


@celery_app.on_after_configure.connect
def newsletter(sender, **kwargs):
    """
    Функция, которая раз в неделю запускает другую
    функцию - bulk_send_newsletter():
    функцию еженедельной отправки писем всем подписчикам
    """
    sender.add_periodic_task(
        crontab(day_of_week=1),
        bulk_send_newsletter.s()
    )


@celery_app.task()
def bulk_send_newsletter():
    """
    Функция, которая создаёт группу задач,
    для отправки писем всем подписчикам,
    и запускает эти задачи параллельно в несколько потоков.
    """
    task_group = group(
        send_newsletter_.s(subscriber)
        for subscriber in Subscription.all_subscribers()
    )
    result = task_group.apply_async()
    result.save()


@celery_app.task()
def send_newsletter_(receiver: str):
    """
    Функция для отправки шаблона письма указанному получателю.
    """
    send_newsletter(receiver)
