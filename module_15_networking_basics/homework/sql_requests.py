is_rooms_table_exist_sql = """
SELECT name FROM sqlite_master
    WHERE type = 'table' AND name = 'rooms_table'
"""

is_booking_table_exist_sql = """
SELECT name FROM sqlite_master
    WHERE type = 'table' AND name = 'booking_table'
"""

create_rooms_table_sql = """
CREATE TABLE rooms_table(
            roomId INTEGER PRIMARY KEY AUTOINCREMENT,
            floor INTEGER,
            beds INTEGER,
            guestNum INTEGER,
            price INTERGER
            )
"""

create_booking_table_sql = """
CREATE TABLE booking_table(
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name CHAR(20),
            last_name CHAR(20),
            check_in DATE FORMAT '%Y%m%d',
            check_out DATE FORMAT '%Y%m%d',
            room_id INTEGER,
            FOREIGN KEY (room_id)
                REFERENCES rooms_table (roomId)
            )
"""

booking_room_sql = """
INSERT INTO booking_table(first_name, last_name, check_in, check_out, room_id)
    VALUES (:first_name, :last_name, :check_in, :check_out, :room_id)
"""

insert_room_sql = """
INSERT INTO rooms_table(floor, beds, guestNum, price)
    VALUES (:floor, :beds, :guestNum, :price)
"""

get_all_rooms_sql = """
SELECT roomId, floor, beds, guestNum, price 
    FROM rooms_table
"""

get_vacant_rooms_sql = """
SELECT rt.roomId, rt.floor, rt.beds, rt.guestNum, rt.price 
    FROM rooms_table rt
    LEFT JOIN booking_table bt ON
        rt.roomId = bt.room_id
    WHERE (
            (
                (check_in NOT BETWEEN :check_in AND :check_out) AND 
                (check_out NOT BETWEEN :check_in AND :check_out)
            ) OR
            (
                (check_in is NULL) AND
                (check_out is NULL)
            ) AND 
            (guestNum >= :guests_num)
        )
"""

is_room_vacant_sql = """
SELECT EXISTS(
    SELECT * FROM booking_table
             WHERE room_id = :room_id AND
                   (
                (check_in BETWEEN :check_in AND :check_out) AND
                (check_out BETWEEN :check_in AND :check_out)
            )
) result
"""