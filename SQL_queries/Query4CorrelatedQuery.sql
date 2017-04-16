SELECT *
FROM species as s1
WHERE 
s1.sstatus = [ STATUS ] AND
population < (
    SELECT AVG(population)
    FROM species as s2
    WHERE s1.sstatus = s2.sstatus
)