CREATE TABLE datasets.iris (
sepal_length FLOAT,
sepal_width	FLOAT,
petal_length FLOAT,
petal_width FLOAT,
species CHAR(10)
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/iris.csv'
INTO TABLE datasets.iris
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

CREATE TABLE datasets.titanic (
survived INT NULL,
pclass INT NULL,
sex	VARCHAR(250) NULL,
age INt NULL,
sibsp INT NULL,
parch INT NULL,
fare FLOAT NULL,
embarked VARCHAR(250) NULL,
class VARCHAR(250) NULL,
who VARCHAR(250) NULL,
adult_male BOOL NULL,
deck VARCHAR(250) NULL,
embark_town VARCHAR(250) NULL,
alive VARCHAR(250) NULL,
alone BOOL NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/titanic.csv'
INTO TABLE datasets.titanic
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(survived, pclass, sex, @age_str, sibsp, parch, fare, embarked, class, who, @adult_male_str, @deck_str, embark_town, alive, @alone_str)
SET adult_male = CASE WHEN @adult_male_str = 'True' THEN 1 ELSE 0 END,
    alone = CASE WHEN @alone_str = 'True' THEN 1 ELSE 0 END,
    age = NULLIF(@age_str, ''),
    deck = NULLIF(@deck_str, '');