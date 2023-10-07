import sqlite3

max_avg_grade_sql = """
SELECT a.group_id, round(avg(ag.grade), 2) avg_grade FROM assignments_grades ag
JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
GROUP BY a.group_id
ORDER BY avg_grade
LIMIT 1
"""

students_amount_sql = """
SELECT sg.group_id, COUNT(*) students_amount
FROM students s
JOIN students_groups sg ON s.group_id = sg.group_id
GROUP BY sg.group_id
"""


with sqlite3.connect('../homework.db') as conn:
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute(max_avg_grade_sql)
    group, grade = cursor.fetchone()
    print(f"Класс: {group}; Средняя оценка: {grade}.")

    cursor.execute(students_amount_sql)
    print(*[f"\tGroup: {group}, Students: {students}\n" for group, students in cursor.fetchall()])