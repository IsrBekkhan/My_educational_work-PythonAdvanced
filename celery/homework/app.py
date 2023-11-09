"""
Flask-приложение
"""
from flask import Flask, jsonify, request
from celery import group
from os import listdir, mkdir

from celery_ import process_images
from database import Base, engine, Subscription, Task
from validators import SubscribeForm

from uuid import uuid4


app = Flask(__name__)


@app.route('/blur', methods=['POST'])
def blur():
    """
    Ставит в очередь обработку переданных изображений
    POST
    form-data
        image: <image: file>
        image: <image: file>
        ...
        email: <email: str>
    :return: ID задачи
    """
    if 'image' in request.files:
        images = request.files.getlist('image')
        email = request.form.get('email')

        task_id = str(uuid4())  # Генерируем уникальный идентификатор для задачи

        src_path = task_id
        mkdir(src_path)
        dst_path = f'blur_{task_id}'
        mkdir(dst_path)

        for index, image in enumerate(images):
            image.save(f'{src_path}/{index + 1}. {image.filename}')

        # Создаем группу задач
        task_group = group(
            process_images.s(
                src_filename=f'{src_path}/{filename}',
                dst_filename=f'{dst_path}/{filename}',
                task_id=task_id,
                email=email
            )
            for filename in listdir(src_path)
        )

        # Создаем в БД запись с информацией о группе задачи
        Task.add_task(
            task_id=task_id,
            total_images=len(images),
            status='в процессе обработки',
            email=email
        )

        # Запускаем группу задач и сохраняем ее
        result = task_group.apply_async()
        result.save()

        # Возвращаем пользователю ID группы для отслеживания
        return jsonify(order_id=task_id), 202

    return "Отсутствует фотография для обработки", 400


@app.route('/status/<order_id>', methods=['GET'])
def status(order_id: str):
    """
    Возвращает информацию о задаче:
    прогресс и статус.
    """
    task = Task.get_task_by_task_id(task_id=order_id)
    return jsonify(task_info=task.to_json()), 200


@app.route('/subscribe', methods=['POST'])
def subscribe():
    """
    Пользователь указывает почту и подписывается на рассылку.
    POST
    form-data
        email: <email: str>
    """
    form = SubscribeForm()

    if form.validate_on_submit():
        email = form.email.data
        return jsonify(Subscription.subscribe(email)), 201

    return jsonify(errors=form.errors), 400


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    """
    Пользователь указывает почту и отписывается от рассылки.
    POST
    form-data
        email: <email: str>
    """
    form = SubscribeForm()

    if form.validate_on_submit():
        email = form.email.data
        return jsonify(Subscription.unsubscribe(email)), 200

    return jsonify(errors=form.errors), 400


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)

    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
