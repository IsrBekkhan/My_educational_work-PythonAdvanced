from flask import Flask, request
from json import JSONEncoder, JSONDecoder
from models import room_addition, booking_it, create_tables, get_vacant_rooms, all_rooms_getter

from typing import Dict, Tuple


app = Flask(__name__)


@app.route('/add-room', methods=['POST'])
def add_room() -> Tuple:
    if request.method == 'POST':
        room_data: str = request.get_data(as_text=True)
        room_data: Dict = JSONDecoder().decode(room_data)
        all_rooms = room_addition(room_data)

        return JSONEncoder(indent=4).encode(all_rooms), 200


@app.route('/room', methods=['GET'])
def get_room():
    if request.method == 'GET':
        check_in = request.args.get('checkIn', type=int)
        check_out = request.args.get('checkOut', type=int)
        guests_num = request.args.get('guestsNum', type=int)

        if all((check_in, check_out, guests_num)):
            vacant_rooms = get_vacant_rooms(check_in, check_out, guests_num)
            return JSONEncoder(indent=4).encode(vacant_rooms), 200

        all_rooms = all_rooms_getter()
        return JSONEncoder(indent=4).encode(all_rooms), 200


@app.route('/booking', methods=['POST'])
def booking_room():
    if request.method == 'POST':
        room_data: str = request.get_data(as_text=True)
        room_data: Dict = JSONDecoder().decode(room_data)

        return booking_it(room_data)


if __name__ == '__main__':
    create_tables()
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)