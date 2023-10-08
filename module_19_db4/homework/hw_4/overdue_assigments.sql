SELECT group_id, round(avg(count), 2) avg_count,
       min(count) min_count,
       max(count) max_count
FROM (
    SELECT a.group_id group_id, count(*) count
    FROM assignments a
    JOIN assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id
    WHERE ag.date > a.due_date
    GROUP BY a.assisgnment_id)
GROUP BY group_id
