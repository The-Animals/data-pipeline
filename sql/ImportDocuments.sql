-- To run: mysql db -h 162.246.157.124 -u admin -p --local-infile < ImportDocuments.sql
DROP TABLE documents;

CREATE TABLE documents
(
    Id INT NOT NULL AUTO_INCREMENT,
    DateCode VARCHAR(14) NOT NULL,
    DateString VARCHAR(100),
    Date DATETIME,
    URL VARCHAR(200),
    PRIMARY KEY (Id)
);

LOAD DATA LOCAL INFILE '../raw_data/Documents.csv'
INTO TABLE documents
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'    
IGNORE 1 ROWS;