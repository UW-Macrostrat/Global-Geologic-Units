DROP TABLE IF EXISTS ignimbrite_named_location;
CREATE TABLE ignimbrite_named_location (
  docid text,
  sentid integer,
  phrase text,
  geometry geometry(Point, 4326)
);

