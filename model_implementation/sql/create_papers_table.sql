DROP TABLE IF EXISTS global_geology_paper;
CREATE TABLE global_geology_paper (
  docid text PRIMARY KEY,
  publisher text,
  title text,
  journal JSON,
  author JSON,
  year numeric,
  number text,
  volume text,
  link JSON,
  identifier JSON,
  type text,
  pages text
);

