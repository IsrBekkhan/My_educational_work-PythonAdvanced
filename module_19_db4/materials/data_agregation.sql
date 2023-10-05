SELECT DISTINCT city
FROM customer;


SELECT DISTINCT city,
                full_name
FROM customer;


SELECT count(*)
FROM orders;


SELECT count(*)
FROM orders
WHERE purchase_amount > 800
  AND purchase_amount < 900;


SELECT avg(purchase_amount)
FROM orders;


SELECT round(avg(purchase_amount)) AS averege_purchase_amount
FROM orders;


SELECT sum(purchase_amount) AS total_amount
FROM orders;


SELECT max(purchase_amount) AS max_purchase
FROM orders;


SELECT max(purchase_amount) AS max_purchase,
       m.full_name
FROM orders o
INNER JOIN manager m ON m.manager_id = o.manager_id;


SELECT min(purchase_amount) AS max_purchase,
       m.full_name
FROM orders o
INNER JOIN manager m ON m.manager_id = o.manager_id;


SELECT sum(full_name)
FROM manager;