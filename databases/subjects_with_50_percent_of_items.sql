SELECT LOWER(subject) as subject as items FROM keyword
JOIN map ON map.kword = keyword.kword
GROUP BY LOWER(keyword.subject)
HAVING(COUNT(iid) >= (SELECT COUNT(iid)/2.0 FROM item))