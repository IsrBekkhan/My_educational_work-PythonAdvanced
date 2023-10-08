-- Простой синтаксис
SELECT t.full_name,
       round(avg(ag.grade), 4) avg_grade,
       a.assignment_text
FROM assignments_grades ag
JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
JOIN teachers t ON a.teacher_id = t.teacher_id
GROUP BY ag.assisgnment_id
ORDER BY avg_grade
LIMIT 1;

-- Вариант с использованием вложенного запроса
SELECT teacher_name, min(avg_grade) min_avg_grade, assigment
FROM
(SELECT t.full_name teacher_name,
       round(avg(ag.grade), 4) avg_grade,
       a.assignment_text assigment
FROM assignments_grades ag
JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
JOIN teachers t ON a.teacher_id = t.teacher_id
GROUP BY ag.assisgnment_id)
