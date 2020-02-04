-- To run: mysql db -h 162.246.157.124 -u admin -p --local-infile < ImportMLAs.sql
DROP TABLE mlas;

CREATE TABLE mlas (
    RidingNumber INT NOT NULL,
    RidingName VARCHAR(100) NOT NULL,
    MLATitle VARCHAR(8) NOT NULL,
    MLAFirstName VARCHAR(50) NOT NULL,
    MLALastName VARCHAR(50) NOT NULL,
    Caucus VARCHAR(10) NOT NULL,
    LegislativePhoneNumber VARCHAR(10) NOT NULL,
    RidingPhoneNumber VARCHAR(10) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    PRIMARY KEY (RidingNumber)
);

LOAD DATA LOCAL INFILE '../data/MLAs.csv' 
INTO TABLE mlas
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'    
IGNORE 1 ROWS;