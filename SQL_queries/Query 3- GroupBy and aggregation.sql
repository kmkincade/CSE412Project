SELECT s.Taxon, s.sName, COUNT(c.ConservationID) as "Conservation Count"
FROM species as s, helpedBy as hb, conservation as c
WHERE 
    s.sName = [SPECIES NAME]
    s.Taxon = hb.Taxon AND
    hb.ConservationID = c.ConservationID
GROUP BY s.taxon