DROP TABLE IF EXISTS reporter, item, onpage, report, keyword, map CASCADE;

CREATE TABLE reporter (
	rid numeric(5, 0) PRIMARY KEY,
	fname char(15) NOT NULL,
	lname char(30) NOT NULL,
	spec char(15) NOT NULL,
	syear numeric(4, 0)
);

CREATE TABLE item (
	iid numeric(5, 0) PRIMARY KEY,
	title varchar(50) NOT NULL,
	pdate date NOT NULL,
	stext char(15) NOT NULL,
	ftext char(15) NOT NULL
);

CREATE TABLE onpage (
	iid numeric(5, 0) NOT NULL REFERENCES item(iid),
	pid char(15) NOT NULL,
	fdate date NOT NULL,
	tdate date,
	PRIMARY KEY (iid, pid)
);

CREATE TABLE report (
	iid numeric(5, 0) NOT NULL REFERENCES item(iid),
	rid numeric(5, 0) NOT NULL REFERENCES reporter(rid),
	PRIMARY KEY (iid, rid)
);

CREATE TABLE keyword (
	kword char(15) NOT NULL UNIQUE,
	subject char(15) NOT NULL,
	PRIMARY KEY (kword, subject)
);

CREATE TABLE map (
	iid numeric(5, 0) NOT NULL REFERENCES item(iid),
	kword char(15) NOT NULL REFERENCES keyword(kword),
	PRIMARY KEY (iid, kword)
);