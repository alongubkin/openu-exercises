WITH rids_that_wrote_health AS (
	SELECT DISTINCT rid FROM report
	JOIN map ON map.iid = report.iid
	JOIN keyword ON map.kword = keyword.kword
	WHERE LOWER(subject) = 'health'
), rids_that_didnt_wrote_health AS (
	SELECT DISTINCT rid FROM report
	JOIN map ON map.iid = report.iid
	JOIN keyword ON map.kword = keyword.kword
	WHERE LOWER(subject) <> 'health'
)

SELECT rid FROM report
-- Make sure the reporter wrote only health items
WHERE report.rid IN (SELECT rid FROM rids_that_wrote_health)
AND report.rid NOT IN (SELECT rid FROM rids_that_didnt_wrote_health)
-- Get the reporter that had the most items 
GROUP BY rid ORDER BY items DESC LIMIT 1