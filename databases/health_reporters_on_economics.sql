SELECT DISTINCT fname, lname FROM reporter
	INNER JOIN report ON reporter.rid = report.rid
	INNER JOIN map ON report.iid = map.iid
	INNER JOIN keyword ON map.kword = keyword.kword
	WHERE LOWER(reporter.spec) = 'health' AND LOWER(keyword.subject) = 'economics'