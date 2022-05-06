/*******************

  Create the schema

********************/

CREATE TABLE IF NOT EXISTS portfolio (
username VARCHAR(256) PRIMARY KEY,
email VARCHAR(256) NOT NULL UNIQUE,
phonenum VARCHAR(8),
year_exp INT,
password VARCHAR(64) NOT NULL,
CHECK(length(phonenum) = 8),
CHECK(length(password) >= 8)
);

CREATE TABLE IF NOT EXISTS pet (
petname VARCHAR(32) NOT NULL,
petid VARCHAR(256) PRIMARY KEY,
type VARCHAR(62) NOT NULL,
breed VARCHAR(32) NOT NULL,
username VARCHAR(256) REFERENCES portfolio(username) DEFERRABLE
);

CREATE TABLE IF NOT EXISTS joboffer (
offerid VARCHAR(32) PRIMARY KEY,
price FLOAT,
location VARCHAR(256) NOT NULL,
date_from DATE NOT NULL,
date_to DATE NOT NULL,
petid VARCHAR(256) REFERENCES pet(petid) DEFERRABLE,
UNIQUE (date_from, date_to, petid), 
CHECK(date_to > date_from)
);

CREATE TABLE IF NOT EXISTS pending (
offerid VARCHAR(32) REFERENCES joboffer(offerid) DEFERRABLE,
petsitter VARCHAR(256) REFERENCES portfolio(username) DEFERRABLE,
UNIQUE (offerid, petsitter)
);

CREATE TABLE IF NOT EXISTS transaction (
offerid VARCHAR(32) REFERENCES joboffer(offerid) DEFERRABLE UNIQUE,
petsitter VARCHAR(256) REFERENCES portfolio(username) DEFERRABLE
);

CREATE TABLE IF NOT EXISTS to_rate (
offerid VARCHAR(32) REFERENCES joboffer(offerid) DEFERRABLE UNIQUE,
rating INT,
CHECK (rating >= 0 AND rating <= 5)
);






