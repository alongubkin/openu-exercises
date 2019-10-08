INSERT INTO reporter(rid, fname, lname, spec, syear) VALUES
	(12345, 'Dan', 'Cohen', 'Health', NULL),
	(54321, 'Yossi', 'Levi', 'Health', 2015),
	(56789, 'Dan', 'Cohen', 'politics', 2018),
	(98765, 'Dana', 'Aviv', 'Economics', NULL),
	(44444, 'Ronit', 'Sagiv', 'Health', 2017);
	
INSERT INTO item(iid, title, pdate, stext, ftext) VALUES
	(1, 'title 1', '2019-06-12', 'stxt1', 'ftxt1'),
	(2, 'title 2', '2019-05-30', 'stxt2', 'ftxt2'),
	(3, 'title 3', '2019-06-01', 'stxt3', 'ftxt3'),
	(4, 'title 4', '2018-06-30', 'stxt4', 'ftxt4'),
	(5, 'title 5', '2019-05-10', 'stxt5', 'ftxt5');
	
INSERT INTO onpage(iid, pid, fdate, tdate) VALUES
	(1, 'Main', '2019-06-12', NULL),
	(2, 'Main', '2019-05-30', '2019-05-30'),
	(2, 'Politics', '2019-05-30', NULL),
	(3, 'Politics', '2019-06-01', NULL),
	(4, 'Politics', '2018-06-30', '2018-07-01');
	
INSERT INTO report(iid, rid) VALUES
	(1, 12345),
	(2, 54321),
	(1, 44444),
	(3, 12345),
	(3, 56789),
	(1, 98765),
	(2, 98765);
	
INSERT INTO keyword(kword, subject) VALUES
	('eco1', 'economics'),
	('eco2', 'economics'),
	('eco3', 'Economics'),
	('pol1', 'politics'),
	('pol2', 'Politics'),
	('pol3', 'politics'),
	('heal1', 'health'),
	('heal2', 'health');
	
INSERT INTO map(iid, kword) VALUES 
	(1, 'eco1'),
	(2, 'pol1'),
	(4, 'heal2'),
	(1, 'pol3'),
	(4, 'pol2'),
	(3, 'eco2');