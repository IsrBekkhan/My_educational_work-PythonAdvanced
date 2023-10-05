import datetime
import sqlite3
import random
from typing import Optional

CREATE_DATABASE_QUERY = """
DROP TABLE IF EXISTS 'teachers';
CREATE TABLE 'teachers' (
    teacher_id integer PRIMARY KEY,
    full_name VARCHAR(20)
);

DROP TABLE IF EXISTS 'students_groups';
CREATE TABLE 'students_groups' (
    group_id INTEGER PRIMARY KEY,
    teacher_id INTEGER REFERENCES teachers(teacher_id)
);

DROP TABLE IF EXISTS 'students';
CREATE TABLE 'students' (
    student_id INTEGER PRIMARY KEY,
    full_name VARCHAR(20),
    group_id INTEGER REFERENCES students_groups(group_id)
);

DROP TABLE IF EXISTS 'assignments';
CREATE TABLE 'assignments' (
    assisgnment_id INTEGER PRIMARY KEY,
    teacher_id REFERENCES teachers(teacher_id),
    due_date varchar(255),
    group_id INTEGER REFERENCES students_groups(group_id),
    assignment_text VARCHAR(100)
);
    
DROP TABLE IF EXISTS 'assignments_grades';
CREATE TABLE 'assignments_grades' (
    grade_id INTEGER PRIMARY KEY,
    assisgnment_id INTEGER REFERENCES assignments(assisgnment_id),
    student_id INTEGER REFERENCES students(student_id),
    grade INTEGER,
    date varchar(255)
);
"""

families = """Иванов
Васильев
Петров
Смирнов
Михайлов
Фёдоров
Соколов
Яковлев
Попов
Андреев
Алексеев
Александров
Лебедев
Григорьев
Степанов
Семёнов
Павлов
Богданов
Николаев
Дмитриев
Егоров
Волков
Кузнецов
Никитин
Соловьёв""".split()

name_letters = "абвгдежзиклмнопрстуфхцчшщэюя".upper()
date_format = '%Y-%m-%d'


def _get_random_date(base_date: Optional[str] = None) -> str:
    if base_date is None:
        day = random.randint(1, 30)
        month = random.randint(1, 12)
        try:
            date = datetime.datetime(year=2020, month=month, day=day)
        except ValueError:
            day -= 1
            date = datetime.datetime(year=2020, month=month, day=day)
    else:
        date = datetime.datetime.strptime(base_date, date_format)
        new_date = random.randint(-10, 5)
        if new_date < 0:
            date = date - datetime.timedelta(days=abs(new_date))
        else:
            date = date + datetime.timedelta(days=abs(new_date))
    return date.strftime(date_format)


def _get_random_full_name() -> str:
    is_male = random.choice((True, False))

    family_name = random.choice(families)
    if not is_male:
        family_name += "а"

    first_letter, last_letter = random.choice(name_letters), random.choice(name_letters)
    return f"{family_name} {first_letter}.{last_letter}."


assignment_verbs = """
посчитать
написать
сочинить
прочитать
выучить
изучить
описать
посетить
деконструировать
апробировать
проанализировать
прочувствовать
переписать
""".split()

assignment_nouns = """алгоритмы и структуры данных
история мировых цивилизаций
хлебобулочные изделия
виноградники в Англии
путешествия во времени
быстродействие исчислений на счетах
классику киноч
основы программирования
базы данных
язык запросов SQL
""".split('\n')


def _get_random_assignment_text() -> str:
    return f'{random.choice(assignment_verbs)} {random.choice(assignment_nouns)}'


def generate_database():
    with sqlite3.connect('homework.db') as conn:
        cursor = conn.cursor()
        cursor.executescript(CREATE_DATABASE_QUERY)
        conn.commit()
        teachers = [
            (_get_random_full_name(),) for _ in range(10)
        ]
        conn.executemany(
            """
            INSERT INTO 'teachers'(full_name)
            VALUES (?)
            """,
            teachers
        )
        groups = [(random.randint(1, 10),) for _ in range(20)]
        conn.executemany(
            """
            INSERT INTO 'students_groups'(teacher_id)
            VALUES(?)
            """,
            groups
        )
        students = [
            (_get_random_full_name(), random.randint(1, 20)) for _ in range(400)
        ]
        conn.executemany(
            """
            INSERT INTO 'students'(full_name, group_id)
            VALUES(?, ?)
            """,
            students
        )
        assignments = [
            (
                random.randint(1, 10),
                _get_random_date(),
                random.randint(1, 20),
                _get_random_assignment_text(),
            )
            for _ in range(40)
        ]
        conn.executemany(
            """
            INSERT INTO 'assignments'(teacher_id, due_date, group_id, assignment_text)
            VALUES(?, ?, ?, ?)
            """,
            assignments
        )
        assignments_grades = [
            (
                random.randint(1, 40),
                random.randint(1, 400),
                int(random.uniform(0.0, 10.99)),
                _get_random_date(asgn[1])
            )
            for asgn in assignments
            for _ in range(20)
        ]
        conn.executemany(
            """
            INSERT INTO 'assignments_grades'(assisgnment_id, student_id, grade, date)
            VALUES(?, ?, ?, ?)
            """,
            assignments_grades
        )


if __name__ == '__main__':
    generate_database()
