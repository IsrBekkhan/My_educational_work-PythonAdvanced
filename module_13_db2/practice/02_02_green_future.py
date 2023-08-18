import sqlite3


def get_number_of_lucky_days(c: sqlite3.Cursor, month_number: int) -> float:
    ...


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        percent_of_lucky_days = get_number_of_lucky_days(cursor, 12)
        print(f"В декабре у ребят было {percent_of_lucky_days:.02f}% удачных дня!")
