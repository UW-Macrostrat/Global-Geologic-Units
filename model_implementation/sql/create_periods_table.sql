DROP TABLE IF EXISTS macrostrat_period;
CREATE TABLE macrostrat_period (
  int_id integer PRIMARY KEY,
  name text,
  abbrev text,
  t_age numeric,
  b_age numeric,
  int_type text,
  timescales text,
  color text
);
COPY macrostrat_period FROM :filename WITH (HEADER, FORMAT 'csv');
