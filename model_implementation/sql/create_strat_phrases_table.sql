DROP TABLE IF EXISTS strat_phrases;
CREATE TABLE strat_phrases (
  docid text,
  sentid integer,
  strat_flag text,
  strat_name_full text,
  strat_mention text,
  flag_id text,
  mention_idx text
);