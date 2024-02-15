from factory.alchemy import SQLAlchemyModelFactory
from factory import Faker


from ..main.models import Client, Parking, db


class ClientFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = Faker('first_name')
    surname = Faker('last_name')
    credit_card = Faker('credit_card_number')
    car_number = Faker('license_plate')


class ParkingFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = Faker('address')
    opened = Faker('pybool')
    count_places = Faker('pyint', min_value=1, max_value=10)
    count_available_places = Faker('pyint', min_value=0, max_value=10)
