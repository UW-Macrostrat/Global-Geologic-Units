DROP TABLE IF EXISTS global_geology_location;
CREATE TABLE global_geology_location (
  docid text,
  sentid integer,
  geometry geometry(Point, 4326),
  sentence text
);
