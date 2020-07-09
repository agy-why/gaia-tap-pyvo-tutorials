-- Histogram of TGAS G magnitudes

-- LANGUAGE = PostgreSQL
-- QUEUE = 30s

SELECT gmag * 0.1 AS gmag_bin, COUNT(gmag) AS number
FROM
(
    SELECT FLOOR(phot_g_mean_mag * 10) AS gmag
    FROM gdr1.tgas_source
) AS gmag_tab
GROUP BY gmag;
