DROP TABLE IF EXISTS ignimbrite_location;
CREATE TABLE ignimbrite_location (
  docid text,
  sentid integer,
  geometry geometry(Point, 4326)
);
