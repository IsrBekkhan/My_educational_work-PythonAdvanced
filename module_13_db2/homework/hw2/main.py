import sqlite3
from csv import DictReader


delete_request = """
DELETE FROM table_fees
    WHERE timestamp = :timestamp AND truck_number = :car_number
"""

def delete_wrong_fees(
        cursor_: sqlite3.Cursor,
        wrong_fees_file: str
) -> None:

    with open(wrong_fees_file, 'r') as csv_file:
        wrong_fees: DictReader = DictReader(csv_file, delimiter=',')
        cursor_.executemany(delete_request, wrong_fees)


if __name__ == "__main__":
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        delete_wrong_fees(cursor, "../wrong_fees.csv")
        conn.commit()
