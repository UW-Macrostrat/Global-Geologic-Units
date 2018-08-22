/*
This SQL view joins locations and unit
mentions found close together in the same paper.
It is created by running `bin/run-model join-datasets`.
*/
CREATE OR REPLACE VIEW global_geology_unit_location AS
SELECT
	u.docid,
	u.sentid unit_sentid,
	l.sentid location_sentid,
	u.name,
	u.position,
	u.period,
	l.geometry
FROM global_geology_unit u
JOIN global_geology_location l
  ON u.docid = l.docid
  /* Gets any location in a 20-sentence (!) window centered
     around the unit mention in the text */
 AND u.sentid BETWEEN l.sentid-10 AND l.sentid+10;

