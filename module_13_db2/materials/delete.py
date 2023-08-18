import sqlite3

delete_request: str = """
DELETE FROM `table_stars`;
"""

if __name__ == "__main__":
    with sqlite3.connect("db_stars.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(delete_request)
        conn.commit()
