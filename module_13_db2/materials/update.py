import sqlite3
from typing import Tuple

get_person_balance_by_name_sql: str = """
SELECT balance
    FROM `table_holiday`
    WHERE name = ?;
"""

update_person_balance_by_name_sql: str = """
UPDATE `table_holiday`
    SET balance = ?
    WHERE name = ?;
"""


def get_person_balance_using_name(c: sqlite3.Cursor, name: str) -> int:
    c.execute(get_person_balance_by_name_sql, (name,))
    result: Tuple[int, ] = c.fetchone()
    return result[0]


def update_person_balance_using_name(c: sqlite3.Cursor, name: str, delta: int) -> None:
    old_balance: int = get_person_balance_using_name(c, name)
    new_balance: int = old_balance + delta
    c.execute(update_person_balance_by_name_sql, (new_balance, name))


if __name__ == "__main__":
    with sqlite3.connect("db_holiday.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        balance_before: int = get_person_balance_using_name(cursor, "Вася")
        update_person_balance_using_name(cursor, "Вася", 500)
        balance_after: int = get_person_balance_using_name(cursor, "Вася")
        print(f"balance_before = {balance_before}, balance_after = {balance_after}")
