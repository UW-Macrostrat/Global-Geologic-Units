/*
This returns few results and shouldn't be trusted...
*/
WITH a AS (
SELECT
	*,
	array_to_string(words,' ') AS text
FROM global_geology_sentences_nlp352
)
SELECT * FROM a
WHERE text ~ '(°|◦)'
  -- We don't want temperatures
  AND NOT text ~ '(°|◦) (C|F)'
  -- We don't want structural data
  AND NOT lemmas && ARRAY['dip','strike','orientation', 'striking',
                           'angle', 'trend', 'plunge', 'inclination', 'direction']

