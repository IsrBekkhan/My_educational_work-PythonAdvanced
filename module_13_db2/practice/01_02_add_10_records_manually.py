import sqlite3


def add_10_records_to_table_warehouse(cursor: sqlite3.Cursor) -> None:
    ...


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        add_10_records_to_table_warehouse(cursor)
        conn.commit()
