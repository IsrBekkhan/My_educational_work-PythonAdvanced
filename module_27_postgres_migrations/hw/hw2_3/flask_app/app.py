from flask import Flask, jsonify, request

from typing import Tuple, Callable

from database import POSTGRES_URL, Base, engine
from create_data import create_random_data, get_address

from models import User, Coffee
from schemas import UserForm


app = Flask(__name__)


@app.before_first_request
def before_first_request():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    create_random_data(count=10)


@app.route('/hello', methods=['GET'])
def hello() -> Tuple[Callable, int]:
    return jsonify(message='Hello World!'), 200


@app.route('/db_url', methods=['GET'])
def db_url() -> Tuple[Callable, int]:
    return jsonify(db_url=POSTGRES_URL), 200


@app.route('/users', methods=['POST'])
def add_user() -> Tuple[Callable, int]:
    """
    Добавление нового пользователя
    Тело POST-запроса
    {
        "name": "Андрей",
        "coffee_id": 1
    }
    """
    user_data = UserForm()

    if user_data.validate_on_submit():

        if not Coffee.check_coffee(user_data.coffee_id.data):
            return jsonify(error=f"Кофе с ID-{user_data.coffee_id.data} не существует в БД."), 404

        user = User(name=user_data.name.data,
                    address=get_address(),
                    coffee_id=user_data.coffee_id.data)
        new_user = User.add_user(user)

        return jsonify(new_user), 201

    return jsonify(invalid_input=user_data.errors), 400


@app.route('/coffee/<name>', methods=['GET'])
def get_coffee(name: str) -> Tuple[Callable, int]:
    """
    Поиск кофе по названию
    """
    coffee_list = Coffee.get_coffee(name)

    if coffee_list:
        return jsonify(coffee_list), 200

    return jsonify(error=f'Кофе с названием {name} нет в БД.'), 404


@app.route('/notes', methods=['GET'])
def get_notes() -> Tuple[Callable, int]:
    """
    Список уникальных элементов в заметках к кофе
    """
    return jsonify(Coffee.get_distinct_notes()), 200


@app.route('/users/<country>', methods=['GET'])
def get_country_users(country: str) -> Tuple[Callable, int]:
    """
    Список пользователей, проживающих в запрашиваемом городе
    """
    return jsonify(User.get_users_from(country)), 200


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
