import sqlite3


MANAGER_NAME = 'Иван Совин'
MANAGER_SALARY = 100000

get_salary_request = """
SELECT salary FROM table_effective_manager
    WHERE name = ?
"""

salary_up_request = """
UPDATE table_effective_manager
    SET salary = ?
    WHERE name = ?
"""

delete_request = """
DELETE FROM table_effective_manager
    WHERE name = ?
"""


def ivan_sovin_the_most_effective(
        cursor_: sqlite3.Cursor,
        name_: str,
) -> None:
    if name_ == MANAGER_NAME:
        print('Нельзя вводить своё же ФИО!')
    else:
        cursor_.execute(get_salary_request, (name_, ))
        try:
            current_salary, *_ = cursor_.fetchone()
        except TypeError:
            print('Человек с таким именем у нас не работает')
        else:
            if current_salary * 1.1 < MANAGER_SALARY:
                cursor_.execute(salary_up_request, (current_salary * 1.1, name_))
                print(f'Сотруднику {name_} повышена зарплата.')
            else:
                cursor_.execute(delete_request, (name_, ))
                print(f'Сотрудник {name_} уволен за жадность')


if __name__ == '__main__':
    name: str = input('Введите имя сотрудника: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        ivan_sovin_the_most_effective(cursor, name)
        conn.commit()
