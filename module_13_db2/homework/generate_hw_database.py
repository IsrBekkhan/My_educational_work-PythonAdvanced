import datetime
import random
import secrets
import sqlite3
from typing import Tuple

generate_hw_1_sql = """
DROP TABLE IF EXISTS `table_truck_with_vaccine`;

CREATE TABLE `table_truck_with_vaccine` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp VARCHAR(100) NOT NULL,
    truck_number VARCHAR(100) NOT NULL,
    temperature_in_celsius NUMERIC NOT NULL
);
"""

car_number_letters = "авекмнорстух"


def _get_random_car_number() -> str:
    number_template = "{first_letter}{number:03d}{tail}{region}"

    first_letter = random.choice(car_number_letters)
    tail = random.choice(car_number_letters) + random.choice(car_number_letters)
    number = random.randint(0, 999)
    region = random.choice([47, 48, 77, 78, 147, 178, 777, 778, 13, 11])

    return number_template.format(
        first_letter=first_letter,
        number=number,
        tail=tail,
        region=region,
    )


def _get_random_start_end_date(
        *, start_year=2020, end_year=2021
) -> Tuple[datetime.datetime, datetime.datetime]:
    assert start_year <= end_year

    start = datetime.datetime(
        year=start_year, month=1, day=1, hour=0, minute=0, second=0, microsecond=0
    )
    end = datetime.datetime(
        year=end_year, month=12, day=31, hour=23, minute=59, second=59, microsecond=0
    )

    start_ts, end_ts = int(start.timestamp()), int(end.timestamp())

    random_start_date_ts = random.randint(start_ts, end_ts)
    delay = random.choice([24, 36, 48, 42]) * 60 * 60

    start_date = datetime.datetime.fromtimestamp(random_start_date_ts)
    return start_date, start_date + datetime.timedelta(seconds=delay)


families = """Иванов
Васильев
Петров
Смирнов
Михайлов
Фёдоров
Соколов
Яковлев
Попов
Андреев
Алексеев
Александров
Лебедев
Григорьев
Степанов
Семёнов
Павлов
Богданов
Николаев
Дмитриев
Егоров
Волков
Кузнецов
Никитин
Соловьёв""".split()

name_letters = "абвгдежзиклмнопрстуфхцчшщэюя".upper()


def _get_random_full_name() -> str:
    is_male = random.choice((True, False))

    family_name = random.choice(families)
    if not is_male:
        family_name += "а"

    first_letter, last_letter = random.choice(name_letters), random.choice(name_letters)

    return f"{family_name} {first_letter}.{last_letter}."


def generate_hw_1_db(c: sqlite3.Connection) -> None:
    cursor = conn.cursor()

    cursor.executescript(generate_hw_1_sql)
    c.commit()

    data = []

    for _ in range(10000):
        truck_number = _get_random_car_number()

        start, end = _get_random_start_end_date()

        while start < end:
            temp = random.randint(160, 200) / 10

            if random.randint(0, 1000) < 10:
                temp = random.randint(140, 160) / 10
            elif random.randint(0, 1000) < 10:
                temp = random.randint(140, 160) / 10

            record = (start.isoformat(), truck_number, temp)
            data.append(record)

            start += datetime.timedelta(hours=1)

    random.shuffle(data)

    for i, record in enumerate(data):
        cursor.execute(
            """
                        INSERT INTO 
                            `table_truck_with_vaccine`(timestamp, truck_number, temperature_in_celsius)
                        VALUES 
                            (?, ?, ?)
                        """,
            record,
        )

        if (i + 1) % 100 == 0:
            c.commit()

    c.commit()

    cursor.execute("SELECT COUNT(*) FROM `table_truck_with_vaccine`")
    records_added, *_ = cursor.fetchone()

    print(
        f"generate_hw_1_db> Added {records_added} records to `table_truck_with_vaccine`"
    )


generate_hw2_sql = """
DROP TABLE IF EXISTS `table_fees`;

CREATE TABLE `table_fees` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp VARCHAR(100) NOT NULL,
    truck_number VARCHAR(100) NOT NULL,
    fee_amount INTEGER NOT NULL
);
"""


def generate_hw_2_db(c: sqlite3.Connection) -> None:
    cursor = conn.cursor()

    cursor.executescript(generate_hw2_sql)
    c.commit()

    wrong_fees = []

    start_date, end_date = _get_random_start_end_date()
    start_ts, end_ts = int(start_date.timestamp()), int(end_date.timestamp())

    for it in range(2500):
        car_number = _get_random_car_number()
        ts = random.randint(start_ts, end_ts)
        accident_date = datetime.datetime.fromtimestamp(ts)

        amount_of_money = random.randint(3, 10) * 100

        cursor.execute(
            """
                    INSERT INTO
                        `table_fees`(timestamp, truck_number, fee_amount)
                    VALUES 
                        (?, ?, ?);
                    """,
            (accident_date.isoformat(), car_number, amount_of_money),
        )

        if random.randint(0, 100) < 5:
            wrong_fees.append((car_number, accident_date))

        if (it + 1) % 100 == 0:
            c.commit()

    random.shuffle(wrong_fees)

    with open("wrong_fees.csv", "w") as fo:
        fo.write("car_number,timestamp\n")

        for car_number, timestamp in wrong_fees:
            fo.write(f"{car_number},{timestamp.isoformat()}\n")

    c.commit()

    cursor.execute("SELECT COUNT(*) FROM `table_fees`")
    records_added, *_ = cursor.fetchone()

    print(f"generate_hw_2_db> Added {records_added} records to `table_fees`.")
    print(f"generate_hw_2_db>     number of wrong fees: {len(wrong_fees)}")


generate_hw4_sql = """
DROP TABLE IF EXISTS `table_effective_manager`;

CREATE TABLE `table_effective_manager` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    salary INTEGER NOT NULL
);
"""

insert_new_employee = """
    INSERT INTO 
        `table_effective_manager`(name, salary)
    VALUES 
        (?, ?);
    """


def generate_hw_4_db(c: sqlite3.Connection) -> None:
    cursor = c.cursor()

    cursor.executescript(generate_hw4_sql)
    c.commit()

    cursor.execute(insert_new_employee, ("Иван Совин", 100000))

    i = 0

    while i < 500:
        salary = random.randint(150, 800) * 100

        is_male = random.choice((True, False))

        family_name = random.choice(families)
        if not is_male:
            family_name += "а"

        full_name = _get_random_full_name()

        try:
            cursor.execute(insert_new_employee, (full_name, salary))
        except sqlite3.IntegrityError:
            continue  # in case of UNIQUE constraint violation

        if (i + 1) % 100 == 0:
            c.commit()

        i += 1

    c.commit()

    cursor.execute("SELECT COUNT(*) FROM `table_effective_manager`")
    records_added, *_ = cursor.fetchone()

    print(
        f"generate_hw_4_db> Added {records_added} records to `table_effective_manager`."
    )


generate_hw5_sql = """
DROP TABLE IF EXISTS `uefa_commands`;
DROP TABLE IF EXISTS `uefa_draw`;

CREATE TABLE `uefa_commands` (
    command_number INTEGER PRIMARY KEY,
    command_name VARCHAR(255) NOT NULL,
    command_country VARCHAR(255) NOT NULL,
    command_level VARCHAR(255) NOT NULL
);

CREATE TABLE `uefa_draw` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command_number INTEGER NOT NULL UNIQUE,
    group_number INTEGER NOT NULL,
    FOREIGN KEY (command_number) REFERENCES `uefa_commands` (command_number)
);
"""


def generate_hw_5_db(c: sqlite3.Connection) -> None:
    cursor = c.cursor()

    cursor.executescript(generate_hw5_sql)
    c.commit()

    print(f"generate_hw_5_db> Recreated `uefa_commands` and `uefa_draw`")


generate_hw6_sql = """
DROP TABLE IF EXISTS `table_friendship_employees`;
DROP TABLE IF EXISTS `table_friendship_schedule`;

CREATE TABLE `table_friendship_employees`(
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    preferable_sport VARCHAR(255) NOT NULL
);

CREATE TABLE `table_friendship_schedule` (
    employee_id INTEGER NOT NULL,
    date VARCHAR(255) NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES `table_friendship_employees` (id)
);
"""


def generate_hw_6_db(c: sqlite3.Connection) -> None:
    cursor = c.cursor()

    cursor.executescript(generate_hw6_sql)
    c.commit()

    number_of_people = 366

    # fill `table_friendship_employees`
    people = [_get_random_full_name() for _ in range(number_of_people)]

    for full_name in people:
        preferable_sport = random.choice(
            ["футбол", "хоккей", "шахматы", "SUP сёрфинг", "бокс", "Dota2", "шах-бокс"]
        )

        cursor.execute(
            """
                INSERT INTO
                    `table_friendship_employees`(name, preferable_sport)
                VALUES 
                    (?, ?);
                """,
            (full_name, preferable_sport),
        )

    c.commit()

    # fill `table_friendship_schedule`

    date = datetime.datetime(year=2020, month=1, day=1)
    end_date = datetime.datetime(year=2020, month=12, day=31)

    start_person = 0

    while date <= end_date:
        work_date = date.strftime("%Y-%m-%d")

        people_to_add = []

        for i in range(10):
            person_idx = 1 + (start_person + i) % number_of_people
            people_to_add.append((person_idx, work_date))

        cursor.executemany(
            """
                INSERT INTO
                    `table_friendship_schedule`(employee_id, date)
                VALUES
                    (?, ?);
                """,
            people_to_add,
        )

        date += datetime.timedelta(days=1)
        start_person += 1

    print(f"generate_hw_6_db> Created a work schedule for {number_of_people}")


generate_hw7_sql = """
DROP TABLE IF EXISTS `table_users`;

CREATE TABLE `table_users`(
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
"""


def _get_random_password() -> str:
    return secrets.token_urlsafe(32)


def generate_hw_7_db(c: sqlite3.Connection) -> None:
    cursor = c.cursor()
    cursor.executescript(generate_hw7_sql)
    c.commit()

    cursor.executemany((
        """
        INSERT INTO `table_users` (username, password)
        VALUES (?, ?)
        """
    ), [
        (_get_random_full_name(), _get_random_password()) for _ in range(100)
    ])

    print(f"generate_hw_7_db> Created `table_users`")


if __name__ == "__main__":
    with sqlite3.connect("homework.db") as conn:
        generate_hw_1_db(conn)
        generate_hw_2_db(conn)
        generate_hw_4_db(conn)
        generate_hw_5_db(conn)
        generate_hw_6_db(conn)
        generate_hw_7_db(conn)
