SELECT O.ship name
	FROM Outcomes O
	JOIN Classes C ON C.class = O.ship
UNION
SELECT S.name name
	FROM Ships S
	JOIN Classes C ON C.class = S.name