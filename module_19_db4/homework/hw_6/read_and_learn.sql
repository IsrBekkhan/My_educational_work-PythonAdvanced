SELECT round(avg(grade)) avg_grade
FROM assignments_grades
WHERE assisgnment_id in (
    SELECT assisgnment_id
    FROM assignments
    WHERE assignment_text LIKE 'прочитать%' OR
          assignment_text LIKE 'выучить%'
    )