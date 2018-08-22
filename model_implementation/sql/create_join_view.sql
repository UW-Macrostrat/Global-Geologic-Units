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
 AND u.sentid BETWEEN l.sentid-10 AND l.sentid+10;

