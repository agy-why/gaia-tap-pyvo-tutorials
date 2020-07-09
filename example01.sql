-- Number of TGAS stars with parallax / parallax_error > 10

-- LANGUAGE = PostgreSQL
-- QUEUE = 30s

SELECT COUNT(*)
FROM gdr1.tgas_source
  WHERE parallax / parallax_error > 10;
