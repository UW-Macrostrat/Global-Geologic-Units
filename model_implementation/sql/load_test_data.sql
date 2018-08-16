DROP TABLE IF EXISTS ignimbrites_sentences_nlp352;
CREATE TABLE ignimbrites_sentences_nlp352 (
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
COPY ignimbrites_sentences_nlp352 FROM :filename;
