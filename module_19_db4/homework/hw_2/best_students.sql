SELECT s.full_name student_name, round(avg(ag.grade), 2) avg_grade
FROM assignments_grades ag
JOIN students s ON ag.student_id = s.student_id
GROUP BY ag.student_id
ORDER BY avg_grade DESC
LIMIT 10