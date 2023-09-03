import sqlite3
from typing import Dict, Optional, Tuple

from sql_requests import (create_booking_table_sql, create_rooms_table_sql, is_rooms_table_exist_sql,
                          is_booking_table_exist_sql, insert_room_sql, get_all_rooms_sql, booking_room_sql,
                          is_room_vacant_sql, get_vacant_rooms_sql)


DB_FILENAME = 'hotel.db'


def create_tables(file_name: str = DB_FILENAME):
    with sqlite3.connect(file_name) as connect:
        cursor: sqlite3.Cursor = connect.cursor()
        cursor.execute(is_rooms_table_exist_sql)
        rooms_table_exits: Optional[tuple[str, ]] = cursor.fetchone()

        if not rooms_table_exits:
            cursor.execute(create_rooms_table_sql)

        cursor.execute(is_booking_table_exist_sql)
        booking_table_exists: Optional[tuple[str, ]] = cursor.fetchone()

        if not booking_table_exists:
            cursor.execute(create_booking_table_sql)


def room_addition(room_data: Dict) -> Dict:
    with sqlite3.connect(DB_FILENAME) as connect:
        cursor: sqlite3.Cursor = connect.cursor()
        cursor.execute(insert_room_sql, room_data)

    return all_rooms_getter()


def all_rooms_getter() -> Dict:
    with sqlite3.connect(DB_FILENAME) as connect:
        cursor: sqlite3.Cursor = connect.cursor()
        cursor.execute(get_all_rooms_sql)
        result = cursor.fetchall()

        if result:
            return {"rooms": [
                {'roomId': seq[0],
                 'floor': seq[1],
                 'beds': seq[2],
                 'guestNum': seq[3],
                 'price': seq[4]} for seq in result]
            }


def booking_it(room_data: Dict) -> Tuple[str, int]:
    with sqlite3.connect(DB_FILENAME) as connect:
        cursor: sqlite3.Cursor = connect.cursor()
        parameters = {
            'first_name': room_data['firstName'],
            'last_name': room_data['lastName'],
            'check_in': room_data['bookingDates']['checkIn'],
            'check_out': room_data['bookingDates']['checkOut'],
            'room_id': room_data['roomId']
        }
        if is_room_exist(cursor, room_data['roomId']):

            if is_room_vacant(cursor, parameters):
                cursor.execute(booking_room_sql, parameters)
                return f"Номера с ID:{room_data['roomId']} успешно забронирован!", 200

            return f"Номер с ID:{room_data['roomId']} на запрошенную дату уже занят", 409

        return f"Номера с ID:{room_data['roomId']} не существует", 404


def is_room_exist(cursor_: sqlite3.Cursor, room_id: int) -> bool:
    cursor_.execute("""
    SELECT roomId FROM rooms_table
        WHERE roomId = ?
    """,(room_id, )
                    )
    if cursor_.fetchone():
        return True
    return False


def is_room_vacant(cursor_: sqlite3.Cursor, room_data: Dict) -> bool:
    cursor_.execute(is_room_vacant_sql, room_data)
    result = cursor_.fetchone()[0]

    if result == 0:
        return True
    return False


def get_vacant_rooms(check_in: int, check_out: int, guests_num: int) -> Dict:
    with sqlite3.connect(DB_FILENAME) as connect:
        cursor: sqlite3.Cursor = connect.cursor()
        parameters = {
            'check_in': check_in,
            'check_out': check_out,
            'guests_num': guests_num
        }
        cursor.execute(get_vacant_rooms_sql, parameters)
        result = cursor.fetchall()

        return {'rooms': [
                {'roomId': seq[0],
                 'floor': seq[1],
                 'beds': seq[2],
                 'guestNum': seq[3],
                 'price': seq[4]} for seq in result]
            }
