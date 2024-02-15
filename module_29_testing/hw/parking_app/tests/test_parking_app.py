import pytest

from datetime import datetime

from ..main.models import Parking


@pytest.mark.parametrize('route', ['/clients', '/clients/1'])
def test_response_status(route, client) -> None:
    response = client.get(route)
    assert response.status_code == 200


def test_create_client(client) -> None:
    new_client = {
        "name": "John",
        "surname": "Lock",
        "credit_card": "AAAA0000",
        "car_number": "A013EE"
    }
    resp = client.post('/clients', json=new_client)

    assert resp.status_code == 201
    assert resp.json['name'] == new_client['name']
    assert resp.json['surname'] == new_client['surname']
    assert resp.json['id'] == 2


def test_create_parking(client) -> None:
    new_parking = {
        "address": "Гагаринский, Дом 4",
        "count_places": 3
    }
    resp = client.post('/parkings', json=new_parking)

    assert resp.status_code == 201
    assert resp.json['address'] == new_parking['address']
    assert resp.json['id'] == 2


@pytest.mark.parking
def test_take_parking_space(client, db) -> None:
    new_client = {
        "name": "Another",
        "surname": "Lock",
        "credit_card": "AAAA0000",
        "car_number": "A013EE"
    }
    resp = client.post('/clients', json=new_client)

    parking_registration = {
        "client_id": 2,
        "parking_id": 1
    }

    parking: Parking = db.session.query(Parking).get(parking_registration['parking_id'])
    count_before_request = parking.count_available_places

    true_resp = client.post('/client_parkings', json=parking_registration)

    parking: Parking = db.session.query(Parking).get(parking_registration['parking_id'])
    count_after_request = parking.count_available_places

    assert true_resp.status_code == 201  # запись о заезде на парковку клиента успешно создана
    assert count_before_request == count_after_request + 1  # количество свободных мест уменьшается


@pytest.mark.parking
def test_is_exception_for_exist_record(client) -> None:
    parking_registration = {
        "client_id": 1,
        "parking_id": 1
    }
    resp = client.post('/client_parkings', json=parking_registration)

    assert resp.status_code == 400  # дублирование записи не допускается


@pytest.mark.parking
def test_is_exception_for_wrong_client(client) -> None:
    parking_registration = {
        "client_id": 2,
        "parking_id": 1
    }
    resp = client.post('/client_parkings', json=parking_registration)

    assert resp.status_code == 400  # запись не существующего клиента не допускается


@pytest.mark.parking
def test_is_exception_for_wrong_parking(client) -> None:
    parking_registration = {
        "client_id": 1,
        "parking_id": 2
    }
    resp = client.post('/client_parkings', json=parking_registration)

    assert resp.status_code == 400  # запись с несуществующей парковкой не допускается


@pytest.mark.parking
def test_leave_parking(client, db) -> None:
    record_for_delete = {
        "client_id": 1,
        "parking_id": 1
    }
    parking: Parking = db.session.query(Parking).get(record_for_delete['parking_id'])
    count_before_request = parking.count_available_places

    resp = client.delete('/client_parkings', json=record_for_delete)

    parking: Parking = db.session.query(Parking).get(record_for_delete['parking_id'])
    count_after_request = parking.count_available_places

    assert resp.status_code == 200  # запись о заезде на парковку клиента успешно удалена
    assert count_before_request == count_after_request - 1  # количество свободных мест увеличивается

    time_in = datetime.strptime(resp.json['time_in'], '%Y-%m-%dT%H:%M:%S.%f')
    time_out = datetime.strptime(resp.json['time_out'], '%Y-%m-%dT%H:%M:%S.%f')

    assert time_in < time_out  # время выезда больше времени заезда


@pytest.mark.parking
def test_is_take_busy_parking_space(client, db) -> None:
    new_parking = {
        "address": "Гагаринский, Дом 5",
        "count_places": 1
    }
    parking_registration = {
        "client_id": 1,
        "parking_id": 2
    }

    parking_resp = client.post('/parkings', json=new_parking)
    registration_resp = client.post('/client_parkings', json=parking_registration)

    parking: Parking = db.session.query(Parking).get(parking_registration['parking_id'])

    assert not parking.opened  # парковка закрывается для новых клиентов, если нет свободных мест


def test_app_config(app):
    assert not app.config['DEBUG']
    assert app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == "sqlite://"
    assert not app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]
