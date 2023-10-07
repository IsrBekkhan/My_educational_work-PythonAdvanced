-- Одни вложенные запросы и агрегатные функции
SELECT full_name
FROM students
WHERE group_id in (
        SELECT group_id
        FROM students_groups
        WHERE teacher_id = (
                SELECT teacher_id
                FROM assignments
                WHERE assisgnment_id = (
                        SELECT assisgnment_id
                        FROM (
                            SELECT assisgnment_id, max(avg_grade)
                            FROM (
                                SELECT assisgnment_id, round(avg(grade), 2) avg_grade
                                FROM assignments_grades
                                GROUP BY assisgnment_id
                            )
                        )
                )
        )
);

-- Чуть короткий вариант
SELECT full_name
FROM students
WHERE group_id in (
        SELECT group_id
        FROM students_groups
        WHERE teacher_id = (
                SELECT teacher_id
                FROM assignments
                WHERE assisgnment_id = (
                        SELECT assisgnment_id
                        FROM (
                                SELECT assisgnment_id, round(avg(grade), 2) avg_grade
                                FROM assignments_grades
                                GROUP BY assisgnment_id
                                ORDER BY avg_grade DESC
                                LIMIT 1
                        )
                )
        )
);

-- C использованием вложенных запросов и JOIN
SELECT *
FROM students_groups sg
JOIN students s ON sg.group_id = s.group_id
WHERE sg.teacher_id = (
        SELECT teacher
        FROM (
            SELECT a.teacher_id teacher, avg(ag.grade) avg_grade
            FROM assignments a
            JOIN assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id
            GROUP BY ag.assisgnment_id
            ORDER BY avg_grade DESC
            LIMIT 1
        )
);




