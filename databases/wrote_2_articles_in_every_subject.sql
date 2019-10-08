WITH items_per_reporter_subject AS (
	SELECT report.rid, LOWER(keyword.subject) AS subject, COUNT(DISTINCT report.iid) as items FROM report
		JOIN map ON map.iid = report.iid
		JOIN keyword ON keyword.kword = map.kword
		GROUP BY report.rid, LOWER(keyword.subject)
)
SELECT rid FROM items_per_reporter_subject
 	WHERE items >= 2
 	GROUP BY rid
 	HAVING(COUNT(subject) IN (SELECT COUNT(DISTINCT LOWER(subject)) FROM keyword))
