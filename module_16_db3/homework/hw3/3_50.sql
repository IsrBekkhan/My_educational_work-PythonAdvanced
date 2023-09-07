SELECT DISTINCT O.battle battle
	FROM Outcomes O
	JOIN Ships S ON S.name = O.ship
	WHERE S.class = 'Kongo'