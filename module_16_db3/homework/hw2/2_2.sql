SELECT c.full_name
    FROM 'customer' c
    LEFT OUTER JOIN 'order' o ON c.customer_id = o.customer_id
    WHERE o.date IS NULL