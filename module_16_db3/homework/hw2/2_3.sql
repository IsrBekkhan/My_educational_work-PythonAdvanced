SELECT o.order_no, m.full_name seller_name, c.full_name buyer_name
    FROM "order" o
    JOIN customer c ON o.customer_id = c.customer_id
    JOIN manager m ON o.manager_id = m.manager_id
    WHERE c.city != m.city