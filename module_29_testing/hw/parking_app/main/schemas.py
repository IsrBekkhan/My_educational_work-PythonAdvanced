from marshmallow import Schema, fields, validate, post_load, ValidationError

from typing import Union

from .models import Client, Parking, ClientParking, db


class ClientSchema(Schema):

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=50))
    surname = fields.Str(required=True, validate=validate.Length(max=50))
    credit_card = fields.Str(validate=validate.Length(max=50))
    car_number = fields.Str(required=True, validate=validate.Length(max=10))

    @post_load
    def create_client(self, data: dict, **kwargs) -> Client:
        client = db.session.query(Client).filter(
            Client.name == data["name"],
            Client.surname == data["surname"]
        ).one_or_none()

        if client is not None:
            raise ValidationError(
                f"Клиент с именем {data['name']} и фамилией {data['surname']} уже существует в БД."
            )

        return Client(**data)


class ParkingSchema(Schema):

    id = fields.Int(dump_only=True)
    address = fields.Str(required=True, validate=validate.Length(max=100))
    count_places = fields.Int(required=True, validate=validate.Range(min=1))

    @post_load
    def create_parking(self, data: dict, **kwargs) -> Parking:
        parking = db.session.query(Parking).filter(
            Parking.address == data["address"]
        ).one_or_none()

        if parking is not None:
            raise ValidationError(
                f"Парковка с адресом {data['address']} уже есть в БД"
            )

        return Parking(**data)


class ClientParkingEntrySchema(Schema):

    id = fields.Int(dump_only=True)
    client_id = fields.Int(required=True)
    parking_id = fields.Int(required=True)
    time_in = fields.DateTime(dump_only=True)

    @post_load
    def create_parking(self, data: dict, **kwargs) -> ClientParking:

        if db.session.query(Client).get(data["client_id"]) is None:
            raise ValidationError(f"Клиента с ID-{data['client_id']} не существует в БД")

        parking: Union[Parking, None] = db.session.query(Parking).get(data["parking_id"])

        if parking is None:
            raise ValidationError(f"Парковки с ID-{data['parking_id']} не существует в БД")

        if not parking.opened:
            raise ValidationError(
                f"Парковка с ID-{data['parking_id']} на данный момент закрыта из-за отсутствия свободных мест"
            )

        return ClientParking(**data)


class ClientParkingLeaveSchema(Schema):

    id = fields.Int(dump_only=True)
    client_id = fields.Int(required=True)
    parking_id = fields.Int(required=True)
    time_in = fields.DateTime(dump_only=True)
    time_out = fields.DateTime(dump_only=True)

    @post_load
    def create_parking(self, data: dict, **kwargs) -> ClientParking:
        client_parking = db.session.query(ClientParking).filter(
            ClientParking.client_id == data["client_id"],
            ClientParking.parking_id == data["parking_id"]
        ).one_or_none()

        if client_parking is None:
            raise ValidationError(
                    f"Запись с комбинацией (ID-клиента = {data['client_id']}, "
                    f"ID-парковки = {data['parking_id']}) не существует в БД"
            )

        if client_parking.client.credit_card is None:
            raise ValidationError(
                f"Отсутствует номер кредитной карты клиента с ID-{data['client_id']}"
            )

        return client_parking
