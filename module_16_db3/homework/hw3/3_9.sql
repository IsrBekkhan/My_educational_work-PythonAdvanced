SELECT DISTINCT p.maker
	FROM pc
	JOIN product p ON p.model = pc.model
	WHERE pc.speed >= 450