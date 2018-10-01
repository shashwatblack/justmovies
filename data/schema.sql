-- FIRST DROP EVERYTHING -------------------------------------------
DO $$ DECLARE
    record RECORD;
BEGIN
    FOR record IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(record.tablename) || ' CASCADE';
    END LOOP;
END $$;

-- COUNTRY ---------------------------------------------------------
CREATE TABLE country(
    pk SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- RATING ----------------------------------------------------------
CREATE TABLE rating(
    pk SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL
);

-- LANGUAGE --------------------------------------------------------
CREATE TABLE language(
    pk SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- ROLENAME --------------------------------------------------------
CREATE TABLE role_name(
    pk SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- PERSON ----------------------------------------------------------
CREATE TABLE person(
    pk SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    dob DATE,
    awards TEXT
);

-- ROLE ------------------------------------------------------------
CREATE TABLE role(
    pk SERIAL PRIMARY KEY,
    role_name INTEGER REFERENCES role_name(pk),
    person INTEGER REFERENCES person(pk)
);

-- MOVIE -----------------------------------------------------------
CREATE TABLE movie(
    pk SERIAL PRIMARY KEY,
	title VARCHAR(500) NOT NULL,
	year SMALLINT,
	plot TEXT,
	imdbRating VARCHAR(10),
	imdbID VARCHAR(50),
	poster VARCHAR(1000),
	country INTEGER REFERENCES country(pk),
	rating INTEGER REFERENCES rating(pk),
	language INTEGER REFERENCES language(pk)
);

-- INVOLVEMENT -----------------------------------------------------
CREATE TABLE involvement(
    pk SERIAL PRIMARY KEY,
    person INTEGER REFERENCES person(pk),
    movie INTEGER REFERENCES movie(pk)
);

-- REVIEW ----------------------------------------------------------
CREATE TABLE review(
    pk SERIAL PRIMARY KEY,
    -- user INTEGER REFERENCES user(pk), -- we don't have users yet
    movie INTEGER REFERENCES movie(pk),
    text TEXT,
    rating SMALLINT,
    constraint rating_range_check check(rating >= 1 and rating <= 10)
);