from flask import Flask, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from typing import List, Tuple, Callable, Union
from datetime import datetime

from .models import db
from .schemas import ClientSchema, ParkingSchema, ClientParkingEntrySchema, ClientParkingLeaveSchema


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking_table.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .models import Client, Parking, ClientParking

    @app.before_first_request
    def before_request_func():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route('/clients', methods=['GET'])
    def get_all_clients() -> Tuple[Callable, int]:
        """
        Получить список всех клиентов из БД
        """
        clients: List[Client] = db.session.query(Client).all()
        clients_list = [client.to_json() for client in clients]
        return jsonify(clients_list), 200

    @app.route('/clients/<int:client_id>', methods=['GET'])
    def get_client_by_id(client_id: int) -> Tuple[Union[str, Callable], int]:
        """
        Получить клиента по заданному id
        """
        client: Client = db.session.query(Client).get(client_id)
        if client is None:
            return f'Клиент с ID-{client_id} не найден', 404

        return jsonify(client.to_json()), 200

    @app.route('/clients', methods=['POST'])
    def create_client() -> Tuple[Callable, int]:
        """
        Добавление нового клиента в БД

        Тело POST-запроса
        {
            "name": "string",
            "surname": "string",
            "credit_card": "string",
            "car_number": "string"
        }
        """
        data = request.json
        schema = ClientSchema()

        try:
            client: Client = schema.load(data)
        except ValidationError as exc:
            return jsonify(exc.messages), 400

        db.session.add(client)
        db.session.commit()

        return schema.dump(client), 201

    @app.route('/parkings', methods=['POST'])
    def create_parking() -> Tuple[Callable, int]:
        """
        Добавление парковки в БД

        Тело POST-запроса
        {
            "address": "Гагарина дом 2",
            "count_places": 100
        }
        """
        data = request.json
        schema = ParkingSchema()

        try:
            parking: Parking = schema.load(data)
        except ValidationError as exc:
            return jsonify(exc.messages), 400

        parking.count_available_places = parking.count_places
        parking.opened = True

        db.session.add(parking)
        db.session.commit()

        return schema.dump(parking), 201

    @app.route('/client_parkings', methods=['POST'])
    def take_parking_space() -> Tuple[Callable, int]:
        """
        Заезд и занятие клиентом парковочного места

        Тело POST-запроса
        {
            "client_id": int,
            "parking_id": int
        }
        """

        data = request.json
        schema = ClientParkingEntrySchema()

        try:
            client_parking: ClientParking = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        # уменьшаем количество доступных мест на 1
        parking: Parking = db.session.query(Parking).get(client_parking.parking_id)
        parking.count_available_places -= 1

        # если нет свободных мест - закрываем парковку
        if parking.count_available_places == 0:
            parking.opened = False

        # записываем дату и время заезда на парковку
        client_parking.time_in = datetime.now()
        db.session.add(client_parking)

        # если такая запись уже существует - отменяем транзакцию
        try:
            db.session.commit()
        except IntegrityError as exc:
            db.session.rollback()
            return jsonify(
                f"Запись о том, что клиент с ID-{client_parking.client_id} занял "
                f"парковку с ID-{client_parking.parking_id} уже существует в БД"
            ), 400

        return schema.dump(client_parking), 201

    @app.route('/client_parkings', methods=['DELETE'])
    def leave_parking() -> Tuple[Callable, int]:
        """
        Выезд клиента с парковки

        Тело POST-запроса
        {
            "client_id": int,
            "parking_id": int
        }
        """

        data = request.json
        schema = ClientParkingLeaveSchema()

        try:
            client_parking: ClientParking = schema.load(data)
        except ValidationError as exc:
            return jsonify(exc.messages), 400

        if client_parking.parking.count_available_places < client_parking.parking.count_places:
            client_parking.parking.count_available_places += 1
            client_parking.parking.opened = True

        client_parking.time_out = datetime.now()
        db.session.delete(client_parking)
        db.session.commit()

        return schema.dump(client_parking), 200

    return app
