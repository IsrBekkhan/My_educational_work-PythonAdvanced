SELECT total_students_counts.group_id AS group_id,
       total_students_counts.students_count AS students_count,
       average_grades.avg_grade AS average_grade,
       not_passed_counts.count AS not_passed_count,
       over_deadline_table.count AS over_deadline_count,
       retries_tabel.count_sum AS retries_count_sum
FROM (
    -- Общее количество учеников в группах
    SELECT group_id, COUNT(*) students_count
    FROM students
    GROUP BY group_id) AS total_students_counts
JOIN (
    -- Средняя оценка
    SELECT s.group_id group_id, round(avg(ag.grade), 2) avg_grade
    FROM assignments_grades ag
    JOIN students s ON ag.student_id = s.student_id
    GROUP BY s.group_id) AS average_grades
    ON total_students_counts.group_id = average_grades.group_id
JOIN (
    -- Количество учеников, которые не сдали работы (оценка ниже 6)
    SELECT s.group_id group_id, COUNT(DISTINCT ag.student_id) count
    FROM assignments_grades ag
    JOIN students s ON ag.student_id = s.student_id
    WHERE ag.grade < 6
    GROUP BY s.group_id) AS not_passed_counts
    ON not_passed_counts.group_id = total_students_counts.group_id
JOIN (
    -- Количество учеников, которые просрочили дедлайн
    SELECT s.group_id group_id, COUNT(DISTINCT ag.student_id) count
    FROM assignments_grades ag
    JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
    JOIN students s ON ag.student_id = s.student_id
    WHERE ag.date > a.due_date
    GROUP BY s.group_id) over_deadline_table
    ON over_deadline_table.group_id = total_students_counts.group_id
JOIN (
    -- Количество повторных попыток сдать работу
    SELECT s.group_id group_id, sum(count) count_sum
    FROM students s
    JOIN (
            SELECT ag.student_id AS student, COUNT(*) - 1 AS count
            FROM assignments_grades ag
            GROUP BY student_id
            HAVING count != 0
            ) ON student = s.student_id
    GROUP BY s.group_id) AS retries_tabel
    ON retries_tabel.group_id = total_students_counts.group_id;
