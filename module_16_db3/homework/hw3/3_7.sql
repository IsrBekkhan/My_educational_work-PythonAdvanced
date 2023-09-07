SELECT p.model model, l.price price
	FROM product p
	JOIN laptop l ON l.model = p.model
	WHERE p.maker = 'B'
UNION
SELECT p.model model, pc.price price
	FROM product p
	JOIN pc ON pc.model = p.model
	WHERE p.maker = 'B'
UNION
SELECT p.model model, pr.price price
	FROM product p
	JOIN printer pr ON pr.model = p.model
	WHERE p.maker = 'B'