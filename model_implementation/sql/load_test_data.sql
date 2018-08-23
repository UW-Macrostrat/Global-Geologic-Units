DROP TABLE IF EXISTS global_geology_sentences_nlp352;
CREATE TABLE global_geology_sentences_nlp352 (
  docid text,
  sentid integer,
  wordidx integer[],
  words text[],
  poses text[],
  ners text[],
  lemmas text[],
  dep_paths text[],
  dep_parents integer[]
);
COPY global_geology_sentences_nlp352 FROM :filename;

CREATE OR REPLACE VIEW global_geology_sentences_plaintext AS
SELECT
  docid,
  sentid,
  array_to_string(words, ' ') AS text
FROM global_geology_sentences_nlp352;
