-- Список уникальных элементов в заметках к кофе
SELECT array_agg(distinct notes)
from (SELECT unnest(coffee.notes) as notes FROM coffee);

-- Список пользователей, проживающих в запрашиваемом городе
SELECT *
FROM users
WHERE address::json ->> 'country' @@ 'Hungary';
