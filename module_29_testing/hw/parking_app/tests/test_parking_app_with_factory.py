from .factories import ClientFactory, ParkingFactory, Client, Parking


def test_create_client(db) -> None:
    new_client = ClientFactory()
    db.session.commit()

    assert new_client.id == 2
    assert len(db.session.query(Client).all()) == 2


def test_create_parking(db) -> None:
    new_parking = ParkingFactory()
    db.session.commit()

    assert new_parking.id == 2
    assert len(db.session.query(Parking).all()) == 2
