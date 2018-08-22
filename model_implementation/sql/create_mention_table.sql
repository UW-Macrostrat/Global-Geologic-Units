DROP TABLE IF EXISTS global_geology_mention;
CREATE TABLE global_geology_mention (
  docid text,
  sentid integer,
  word text,
  wordidx integer,
  refs text[],
  ref_poses text[]
);
