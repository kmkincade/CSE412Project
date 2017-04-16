SELECT h.Biome, h.Country, COUNT(s.Taxon) as 'Species Count'
FROM habitat as h, species as s, livesIn as li
WHERE
    s.Taxon = li.Taxon AND
    h.HabitatID = li.HabitatID
GROUP BY h.HabitatID
/* HAVING COUNT(s.Taxon) > N */