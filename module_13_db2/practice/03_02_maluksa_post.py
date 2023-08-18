import sqlite3

sql_script_to_execute = "..."

if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        cursor.executescript(sql_script_to_execute)
        conn.commit()
