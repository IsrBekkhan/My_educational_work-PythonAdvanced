import pytest

from datetime import datetime

from ..main.app import create_app
from ..main.models import Client, Parking, ClientParking, db as _db


@pytest.fixture
def app():
    _app = create_app()
    _app.config['TESTING'] = True
    _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    _app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with _app.app_context():
        _db.create_all()

        client = Client(
            name='Testname',
            surname='Testsurname',
            credit_card='4444 5555 6666 7777',
            car_number='A103EE'
        )
        parking = Parking(
            address='Гагаринский, Дом 3',
            opened=True,
            count_places=3,
            count_available_places=2
        )
        client_parking = ClientParking(
            client_id=1,
            parking_id=1,
            time_in=datetime.now()
        )

        _db.session.bulk_save_objects([client, parking, client_parking])
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
