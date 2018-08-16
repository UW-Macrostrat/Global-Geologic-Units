DROP TABLE IF EXISTS ignimbrite_mention;
CREATE TABLE ignimbrite_mention (
  docid text,
  sentid integer,
  word text,
  wordidx integer,
  refs text[],
  ref_poses text[]
);
