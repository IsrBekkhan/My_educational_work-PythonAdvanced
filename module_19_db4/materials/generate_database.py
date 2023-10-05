import random
import sqlite3

CREATE_TABLES = """
DROP TABLE IF EXISTS 'customer';
CREATE TABLE 'customer' (
    customer_id integer PRIMARY KEY autoincrement,
    full_name varchar(50) NOT NULL,
    city varchar(50) NOT NULL,
    manager_id integer REFERENCES manager(manager_id)
);


DROP TABLE IF EXISTS 'manager';
CREATE TABLE 'manager' (
   manager_id integer PRIMARY KEY autoincrement,
   full_name varchar(50) NOT NULL,
   city varchar(50) NOT NULL
);
   
DROP TABLE IF EXISTS 'orders';
CREATE TABLE 'orders' (
    order_no integer PRIMARY KEY autoincrement,
    purchase_amount integer NOT NULL, 
    date varchar(255) NOT NULL,
    customer_id integer REFERENCES customer(customer_id),
    manager_id integer REFERENCES manager(manager_id)
);
"""


def _get_random_date() -> str:
    day = random.randint(1, 30)
    month = random.randint(1, 12)
    return f"2020-{month}-{day}"


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


cities = """
Москва
Омск
Барнаул
Ярославль
Краснодар
Севастополь
Ялта
Сочи
Ижевск
Иркутск
Мурманск
Санкт-Петербург
Архангельск
""".split()


def prepare_tables():
    with sqlite3.connect("SalesInfo.db") as conn:
        cursor = conn.cursor()
        cursor.executescript(CREATE_TABLES)
        conn.commit()
        managers = [
            (_get_random_full_name(), random.choice(cities))
            for _ in range(30)
        ]
        conn.executemany(
            """
                INSERT INTO 'manager'(full_name, city)
                VALUES (?, ?)
            """,
            managers
        )

        customers = [
            (
                _get_random_full_name(),
                random.choice(cities),
                random.choice([i for i in range(1, 21)] + [None])
            )
            for _ in range(500)
        ]
        conn.executemany(
            """
                INSERT INTO 'customer'(full_name, city, manager_id)
                VALUES(?, ?, ?)
            """,
            customers
        )

        orders = [
            (
                random.randint(10, 1000),
                _get_random_date(),
                random.randint(1, 100),
                random.choice([i for i in range(1, 21)] + [None])
            )
            for _ in range(10000)
        ]

        conn.executemany(
            """
                INSERT INTO 'orders'(purchase_amount, date, customer_id, manager_id)
                VALUES(?, ?, ?, ?)
            """,
            orders
        )


if __name__ == '__main__':
    prepare_tables()
