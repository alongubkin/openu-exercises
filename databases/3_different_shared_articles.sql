-- Create a map between an item to the amount of reporters that wrote it
WITH items_reporters AS (
	SELECT iid, COUNT(rid) AS reporters FROM report
	GROUP BY iid
)

SELECT reporter.rid, fname, lname FROM reporter
	JOIN report ON reporter.rid = report.rid
	-- Each article must have one other reporter
	WHERE report.iid IN (SELECT iid FROM items_reporters WHERE reporters >= 2)
	GROUP BY reporter.rid
	-- Each reporter must have 3 different articles of that type
	HAVING (COUNT(report.iid) >= 3)