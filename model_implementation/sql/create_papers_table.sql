DROP TABLE IF EXISTS ignimbrite_paper;
CREATE TABLE ignimbrite_paper (
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

