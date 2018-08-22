DROP TABLE IF EXISTS global_geology_named_location;
CREATE TABLE global_geology_named_location (
  docid text,
  sentid integer,
  phrase text,
  geometry geometry(Point, 4326)
);

