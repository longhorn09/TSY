create table TSY_HISTORICALS(
	ID int NOT NULL AUTO_INCREMENT,
    URL varchar(100) DEFAULT NULL,
    TSY_DATE date DEFAULT NULL,
    `1MO` double DEFAULT NULL,
    `2MO` double DEFAULT NULL,
    `3MO` double DEFAULT NULL,
    `6MO` double DEFAULT NULL,
    `1Y` double DEFAULT NULL,
    `2Y` double DEFAULT NULL,
    `3Y` double DEFAULT NULL,
    `5Y` double DEFAULT NULL,
    `7Y` double DEFAULT NULL,
    `10Y` double DEFAULT NULL,
    `20Y` double DEFAULT NULL,
    `30Y` double DEFAULT NULL,    
	PRIMARY KEY(ID)
);
	