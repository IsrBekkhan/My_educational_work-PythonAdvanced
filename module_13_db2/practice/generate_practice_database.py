import datetime
import random
import sqlite3

practice_2_sql = """
DROP TABLE IF EXISTS `table_warehouse`;

CREATE TABLE `table_warehouse` (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    amount INTEGER
);

INSERT INTO `table_warehouse` (name, description, amount)
    VALUES ('Огурцы', 'Сушёные, с перцем, из Вологды', 5000);
"""

practice_3_sql = """
DROP TABLE IF EXISTS `table_books`;

CREATE TABLE `table_books` (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_name VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    publish_year INTEGER NOT NULL,
    ISBN VARCHAR(255) NOT NULL UNIQUE
);
"""

practice_4_sql = """
DROP TABLE IF EXISTS `table_kotlin`;

CREATE TABLE `table_kotlin` (
    check_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts VARCHAR(100) NOT NULL,
    wind INTEGER NOT NULL
);
"""


def practice_4_generate_data(c: sqlite3.Cursor) -> None:
    date = datetime.datetime(year=1710, day=17, month=6)
    end_date = datetime.datetime.now()

    while date < end_date:
        wind_speed = max(1, int(random.gauss(12, 33)))
        c.execute(
            "INSERT INTO `table_kotlin` (ts, wind) VALUES (?, ?)",
            (date.isoformat(), wind_speed),
        )

        date = date + datetime.timedelta(days=1)


plactice_5_sql = """
DROP TABLE IF EXISTS `table_green_future`;

CREATE TABLE `table_green_future` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date VARCHAR(128) NOT NULL,
    action VARCHAR(256) NOT NULL
);
"""


def practice_5_generate_data(c: sqlite3.Cursor) -> None:
    actions = [
        "мешок пластика",
        "мешок алюминия",
        "отнесли мешки на завод",
        "выпили кофе с Старбакс",
    ]
    this_year = datetime.datetime.now().year
    date_start = datetime.datetime(year=this_year - 1, month=1, day=1)
    end_date = datetime.datetime(year=this_year, month=1, day=1)

    current_date = date_start

    while current_date < end_date:
        number_of_actions = random.randint(1, 4)
        current_actions = []

        for _ in range(number_of_actions):
            action = random.choice(actions)

            current_actions.append((current_date.strftime("%Y-%m-%d"), action))

        cursor.executemany("""INSERT INTO `table_green_future`(date,action) VALUES (?, ?);""", current_actions)
        current_date = current_date + datetime.timedelta(days=1)


practice_6_sql = """
DROP TABLE IF EXISTS `table_enemies`;

CREATE TABLE `table_enemies` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE
);
"""


def practice_6_generate_data(c: sqlite3.Cursor) -> None:
    people = [
        "Иванов Э.",
        "Петров Г.",
        "Левченко Л.",
        "Михайлов М.",
        "Яковлев Я",
        "Кузнецов К.",
        "Волков А.",
        "Толстой Л.",
        "Дмитриев Д.",
        "Николаев И.",
        "Алексеев В.",
        "Богданов Х.",
        "Павлов А.",
        "Алексеев К.",
        "Андреев П.",
        "Семёнов И.",
        "Степанов В.",
        "Григорьев Р.",
        "Лебедев А.",
        "Александров Б.",
        "Попов Е.",
    ]
    random.shuffle(people)

    people_to_insert = [(v,) for v in people]

    c.executemany("""INSERT INTO `table_enemies`(name) VALUES (?)""", people_to_insert)


practice_7_sql = """
DROP TABLE IF EXISTS `table_russian_post`;

CREATE TABLE `table_russian_post` (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_day VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL DEFAULT 'Адрес не указан, но и не важен'
);
"""


def practice_7_generate_data(c: sqlite3.Cursor) -> None:
    date = datetime.datetime(year=2020, day=1, month=1)
    end_date = datetime.datetime.now()

    while date <= end_date:
        number_of_delivers = random.randint(1, 10)

        c.executemany(
            """
                INSERT INTO
                    `table_russian_post`(order_day)
                VALUES 
                    (?)
                """,
            [(date.strftime("%d-%m-%Y"),) for _ in range(number_of_delivers)],
        )

        diff_in_days = random.randint(1, 3)
        date += datetime.timedelta(days=diff_in_days)


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()

        cursor.executescript(practice_2_sql)
        cursor.executescript(practice_3_sql)
        cursor.executescript(practice_4_sql)
        practice_4_generate_data(cursor)
        cursor.executescript(plactice_5_sql)
        practice_5_generate_data(cursor)
        cursor.executescript(practice_6_sql)
        practice_6_generate_data(cursor)
        cursor.executescript(practice_7_sql)
        practice_7_generate_data(cursor)
