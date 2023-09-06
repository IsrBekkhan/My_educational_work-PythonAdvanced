SELECT DISTINCT p.maker AS Maker, l.speed AS speed
	FROM laptop l
	JOIN product p ON l.model = p.model
	WHERE hd >= 10
	ORDER BY l.speed