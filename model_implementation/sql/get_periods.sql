-- Get period names that don't have spaces or dashes
SELECT name
FROM macrostrat_period
WHERE name !~ '[ -]';
