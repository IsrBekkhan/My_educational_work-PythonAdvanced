import sqlite3

disting_action = """
SELECT date, COUNT(DISTINCT action) count 
    FROM table_green_future
    WHERE date LIKE ? AND
        (action = 'мешок пластика'
        OR action = 'мешок алюминия'
        OR action = 'отнесли мешки на завод')
    GROUP BY date
"""

days_count = f"""
SELECT COUNT(*) FROM ({disting_action})
"""

best_days_count = f"""
SELECT COUNT(*) FROM ({disting_action})
    WHERE count = 3
"""

sql_request = f"""
SELECT (100 * 1.0) / ({days_count}) * ({best_days_count})
"""

def get_number_of_lucky_days(c: sqlite3.Cursor, month_number: int) -> float:

    if len(str(month_number)) == 1:
        month_number_value = f'2022-0{month_number}-%'
    else:
        month_number_value = f'2022-{month_number}-%'

    cursor.execute(sql_request, (month_number_value, month_number_value ))
    return cursor.fetchone()[0]


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        percent_of_lucky_days = get_number_of_lucky_days(cursor, 12)
        print(f"В декабре у ребят было {percent_of_lucky_days:.02f}% удачных дня!")
