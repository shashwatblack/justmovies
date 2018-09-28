DROP TABLE IF EXISTS rating;

CREATE TABLE rating(
    pk SERIAL PRIMARY KEY,
    name CHAR(20) UNIQUE NOT NULL
);

INSERT INTO rating ("name") VALUES ('B');
INSERT INTO rating ("name") VALUES ('B15');
INSERT INTO rating ("name") VALUES ('G');
INSERT INTO rating ("name") VALUES ('NC-17');
INSERT INTO rating ("name") VALUES ('PG');
INSERT INTO rating ("name") VALUES ('PG-13');
INSERT INTO rating ("name") VALUES ('R');
INSERT INTO rating ("name") VALUES ('TV-14');
INSERT INTO rating ("name") VALUES ('TV-MA');
INSERT INTO rating ("name") VALUES ('TV-PG');
INSERT INTO rating ("name") VALUES ('UNRATED');

SELECT * FROM rating;

-- B
-- B15
-- G
-- N/A
-- NC-17
-- NOT RATED
-- Not specified
-- PG
-- PG-13
-- R
-- TV-14
-- TV-MA
-- TV-PG
-- UNRATED

-- N/A, NOT RATED, Not specified are UNRATED 