import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("sample_database.db") as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM `table_people`")

        result = cursor.fetchall()

        print(result)
