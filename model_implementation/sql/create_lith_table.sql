DROP TABLE IF EXISTS macrostrat_lith;
CREATE TABLE macrostrat_lith (
  lith_id numeric PRIMARY KEY,
  name text,
  type text,
  group text,
  class text,
  color text,
  fill numeric,
  t_units numeric
	);
COPY macrostrat_lith FROM :filename WITH (HEADER, FORMAT 'csv');