SELECT t1.full_name, t2.full_name
    FROM (SELECT * FROM customer) AS t1
    JOIN (SELECT * FROM customer) AS t2
    WHERE t1.full_name != t2.full_name AND
          t1.manager_id = t2.manager_id AND
          t1.city = t2.city