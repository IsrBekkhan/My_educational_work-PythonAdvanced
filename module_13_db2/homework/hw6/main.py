import sqlite3
from datetime import date, timedelta
from typing import Dict, List

get_employees_request = """
SELECT id, name, preferable_sport 
    FROM table_friendship_employees
    WHERE preferable_sport = ?
"""

delete_request = """
DELETE FROM table_friendship_schedule
"""

insert_request = """
INSERT INTO table_friendship_schedule(employee_id, date)
    VALUES (?, ?)
"""

game_schedule = {
    0: 'футбол',
    1: 'хоккей',
    2: 'шахматы',
    3: 'SUP сёрфинг',
    4: 'бокс',
    5: 'Dota2',
    6: 'шах-бокс'
}


def update_work_schedule(cursor_: sqlite3.Cursor) -> None:
    employees_weekday_sorted: Dict[int, List] = dict()

    for key, value in game_schedule.items():
        cursor_.execute(get_employees_request, (value, ))
        employees_weekday_sorted[key] = cursor_.fetchall()

    cursor_.execute(delete_request)
    date_obj = date(year=2020, month=1, day=1)

    for _ in range(366):
        weekday = date_obj.weekday()
        date_str = date_obj.strftime('%Y-%m-%d')
        work_day = (weekday + 1) % 7

        current_10_free_employees = [employees_weekday_sorted[work_day].pop(0) for _ in range(10)]
        employees_weekday_sorted[work_day].extend(current_10_free_employees)

        parameters = [(employee[0], date_str) for employee in current_10_free_employees]
        cursor_.executemany(insert_request, parameters)

        date_obj += timedelta(days=1)
    print('Расписание смен на 365 дней занесено в БД!')


if __name__ == '__main__':
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        update_work_schedule(cursor)
        conn.commit()
