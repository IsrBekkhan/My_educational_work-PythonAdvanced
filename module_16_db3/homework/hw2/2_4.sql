SELECT o.order_no, c.full_name
    FROM "order" o
    JOIN customer c ON o.customer_id = c.customer_id
    WHERE o.manager_id IS NULL