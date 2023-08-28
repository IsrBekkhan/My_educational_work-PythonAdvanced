import sqlite3

orders_getter_sql = """
SELECT order_day FROM table_russian_post
    WHERE order_day LIKE '%-05-2020'
"""
orders_updater_sql = """
UPDATE table_russian_post
    SET order_day = ?
    WHERE order_day = ?
"""


def orders_getter(c: sqlite3.Cursor) -> list:
    c.execute(orders_getter_sql)
    return c.fetchall()

def orders_updater(c: sqlite3.Cursor, data: list) -> None:
    for date in data:
        date_str: str = date[0]
        date_list = date_str.split('-')
        date_list[1] = '06'
        new_date = '-'.join(date_list)
        c.execute(orders_updater_sql, (new_date, date_str))

if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        result = orders_getter(cursor)
        orders_updater(cursor, result)
        conn.commit()
