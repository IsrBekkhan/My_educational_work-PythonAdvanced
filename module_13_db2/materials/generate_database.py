import glob
import os
import random
import sqlite3
from typing import List

materials_1_sql: str = """
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

materials_holiday_sql: str = """
DROP TABLE IF EXISTS `table_holiday`;

CREATE TABLE `table_holiday` (
    person_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    balance INTEGER NOT NULL DEFAULT 0
);

INSERT INTO `table_holiday`
    (name, balance)
    VALUES 
        ('Пётр Иванович', 1500),
        ('Вася', 1000),
        ('Лидочка', 0),
        ('Екатерина Владимировна', 0),
        ('Митя', 0);
"""

materials_stars_sql: str = """
DROP TABLE IF EXISTS `table_stars`;

CREATE TABLE `table_stars` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    distance INTEGER NOT NULL,
    constellation VARCHAR(255) NOT NULL
);

INSERT INTO `table_stars`
    (name, constellation,distance)
    VALUES 
        ('Альфа Центавра', 'центавр', 3),
        ('Бетельгейзе', 'орион', 548),
        ('Сириус', 'большой пёс', 9),
        ('Полярная звезда', 'малая медведица', 447),
        ('Кохаб', 'малая медведица', 126),
        ('Фелькард', 'малая медведица', 480),
        ('Йильдун', 'малая медведица', 172),
        ('Уроделус', 'малая медведица', 300),
        ('Алиф аль Фаркадин', 'малая медведица', 337),
        ('Анвар аль Фаркадин', 'малая медведица', 96),
        ('Адара', 'большой пёс', 431),
        ('Везен', 'большой пёс', 1791),
        ('Мирцам', 'большой пёс', 499),
        ('Алудра', 'большой пёс', 3500),
        ('Ригель', 'орион', 860),
        ('Антарес', 'скорпион', 600)
        ;


"""

materials_school_sql: str = """
DROP TABLE IF EXISTS `table_school`;

CREATE TABLE `table_school` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    class INTEGER NOT NULL,
    amount_of_money INTEGER NOT NULL
);
"""

materials_school_add_person: str = """
    INSERT INTO `table_school` (name, class, amount_of_money)
    VALUES
        (?, ?, ?);
"""

families: List[str] = """Иванов
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

name_start_letters: str = "абвгдежзиклмнопрстуфхцчшщэюя".upper()


def add_person_to_school(db_name: str, number_of_person: int) -> None:
    with sqlite3.connect(db_name) as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        for _ in range(number_of_person):
            is_male: bool = random.choice((True, False))
            family_name: str = random.choice(families)
            if not is_male:
                family_name += "а"

            name_letter: str = random.choice(name_start_letters)
            full_name: str = f"{family_name} {name_letter}."
            class_number: int = random.randint(1, 11)
            amount_of_money: int = random.randint(25, 500) * 10

            cursor.execute(
                materials_school_add_person, (full_name, class_number, amount_of_money)
            )


def cleanup() -> None:
    print("Cleanup following files:")
    this_file_path: str = os.path.abspath(__file__)
    hw_dir_name: str = os.path.dirname(this_file_path)
    for file_name in glob.glob(f"{hw_dir_name}/*.db"):
        print(f"\t{file_name}")
        os.unlink(file_name)


def generate_db(db_name: str, sql_request: str) -> None:
    print(f"Create {db_name}")
    with sqlite3.connect(db_name) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.executescript(sql_request)
        conn.commit()


if __name__ == "__main__":
    cleanup()
    generate_db("db_1.db", materials_1_sql)
    generate_db("db_stars.db", materials_stars_sql)
    generate_db("db_holiday.db", materials_holiday_sql)
    generate_db("db_school.db", materials_school_sql)
    add_person_to_school("db_school.db", 400)
