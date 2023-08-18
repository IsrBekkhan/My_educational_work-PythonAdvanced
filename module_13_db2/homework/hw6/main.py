import sqlite3


def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    ...


if __name__ == '__main__':
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        update_work_schedule(cursor)
        conn.commit()
