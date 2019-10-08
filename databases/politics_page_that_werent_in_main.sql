SELECT item.iid, item.title FROM item
	JOIN onpage ON item.iid = onpage.iid
	WHERE onpage.pid = 'Politics' 
		AND onpage.tdate IS NULL
		AND item.iid NOT IN (
			SELECT iid FROM onpage AS onpage2
			WHERE onpage2.pid = 'Main'
		)