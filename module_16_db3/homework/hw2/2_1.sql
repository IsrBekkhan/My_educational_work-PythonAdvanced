SELECT c.full_name customer,
       m.full_name manager,
       o.purchase_amount,
       o.date
    FROM "order" o
    JOIN customer c ON o.customer_id = c.customer_id
    JOIN manager m ON o.manager_id = m.manager_id