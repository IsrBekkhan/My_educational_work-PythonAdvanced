import sqlite3


max_grade_sql = """
SELECT max(grade) FROM assignments_grades
"""

min_grade_sql = """
SELECT min(grade) FROM assignments_grades
"""

avg_grade_sql = """
SELECT avg(grade) FROM assignments_grades
"""

students_amount_sql = """
SELECT DISTINCT COUNT(*) FROM students
"""

teachers_amount_sql = """
SELECT DISTINCT COUNT(*) FROM teachers
"""


with sqlite3.connect('../homework.db') as conn:
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute(teachers_amount_sql)
    print(cursor.fetchone()[0])