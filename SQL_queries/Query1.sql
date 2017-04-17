SELECT * FROM species WHERE sName = '_name';
SELECT R.* FROM species AS S, relatedReading AS R WHERE S.sName = '_search ' AND R.Taxon = S.Taxon
SELECT H.Taxon, C.cName FROM species AS S, helpedBy AS H, conservation AS C WHERE S.sName = '_search' AND S.Taxon = H.Taxon AND C.ConservationID = H.ConservationID
SELECT H.Biome, H.Country FROM species AS S, livesIn AS L, habitat AS H WHERE S.sName = '" + _search + "' AND S.Taxon = L.Taxon AND L.HabitatID = H.HabitatID
SELECT DISTINCT T.tName FROM destroys AS D, threats AS T, habitat AS H, livesIn AS L, species AS S WHERE S.sName = '_search' AND S.Taxon = L.Taxon AND L.HabitatID = H.HabitatID AND D.HabitatID = H.HabitatID AND D.ThreatID = T.ThreatID
