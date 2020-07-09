-- M4 globular cluster with geometric distances using ADQL

-- LANGUAGE = ADQL
-- QUEUE = 5m

SELECT gaia.source_id, gaia.ra, gaia.dec, gd.r_est
FROM gdr2.gaia_source gaia, gdr2_contrib.geometric_distance gd
  WHERE 1 = CONTAINS(POINT('ICRS', gaia.ra, gaia.dec), 
                   CIRCLE('ICRS',245.8962, -26.5222, 0.5))
    AND gaia.phot_g_mean_mag < 15
    AND gd.r_est BETWEEN 1500 AND 2300
    AND gaia.source_id = gd.source_id
