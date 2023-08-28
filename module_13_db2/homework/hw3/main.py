import datetime
import sqlite3


creat_table_request = """
CREATE TABLE IF NOT EXISTS `table_birds` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_time VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    count INTEGER NOT NULL
);
"""

insert_request = """
INSERT INTO table_birds (date_time, name, count)
    VALUES (?, ?, ?)
"""

is_exists_request = """
SELECT EXISTS (SELECT * FROM table_birds
    WHERE name = ?)
"""


def log_bird(
        cursor_: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
        count_: int
) -> None:
    cursor_.execute(insert_request, (date_time, bird_name.title(), count_))
    print(f'{bird_name} добавлен(а).')


def check_if_such_bird_already_seen(
        cursor_: sqlite3.Cursor,
        bird_name: str
) -> bool:
    cursor_.execute(is_exists_request, (bird_name, ))

    if cursor_.fetchone()[0] == 1:
        return True
    return False


if __name__ == "__main__":
    print("Программа помощи ЮНатам v0.1")
    name: str = input("Пожалуйста введите имя птицы\n> ")
    count_str: str = input("Сколько птиц вы увидели?\n> ")
    count: int = int(count_str)
    right_now: str = datetime.datetime.utcnow().isoformat()

    with sqlite3.connect("../homework.db") as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.executescript(creat_table_request)

        if check_if_such_bird_already_seen(cursor, name):
            print("Такую птицу мы уже наблюдали!")
        else:
            log_bird(cursor, name, right_now, count)
