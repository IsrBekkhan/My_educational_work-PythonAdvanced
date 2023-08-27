import sqlite3
from typing import List

defeated_enemies = [
    "Иванов Э.",
    "Петров Г.",
    "Левченко Л.",
    "Михайлов М.",
    "Яковлев Я",
    "Кузнецов К.",
]

remove_request = """
DELETE FROM table_enemies
WHERE name = ?
"""


def remove_all_defeated_enemies(
        c: sqlite3.Cursor,
        defeated_enemies: List[str]
) -> None:
    for name in defeated_enemies:
        c.execute(remove_request, (name, ))


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        remove_all_defeated_enemies(cursor, defeated_enemies)
        conn.commit()
