DROP TABLE IF EXISTS macrostrat_strat;
CREATE TABLE macrostrat_strat (
  strat_name text,
  strat_name_long text,
  rank text,
  strat_name_id numeric PRIMARY KEY,
  concept_id numeric,
  bed text,
  bed_id text,
  mbr text,
  mbr_id text,
  fm text,
  fm_id text,
  subgp text,
  subgp_id text,
  gp text,
  gp_id text,
  sgp text,
  sgp_id text,
  b_age numeric,
  t_age numeric,
  b_period text,
  t_period text,
  c_interval text,
  t_units text,
  ref_id numeric
);
COPY macrostrat_strat FROM :filename WITH (HEADER, FORMAT 'csv');