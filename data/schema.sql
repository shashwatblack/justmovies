-- FIRST DROP EVERYTHING -------------------------------------------
DO $$ DECLARE
    record RECORD;
BEGIN
    FOR record IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(record.tablename) || ' CASCADE';
    END LOOP;
END $$;
-- DROP TYPES
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'role') THEN
        DROP TYPE role;
    END IF;
END$$;

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

-- GENRE -----------------------------------------------------------
CREATE TABLE genre(
    pk SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- PERSON ----------------------------------------------------------
CREATE TABLE person(
    pk SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    dob DATE,
    image VARCHAR(1000),
    intro TEXT
);

-- ROLE ------------------------------------------------------------
CREATE TYPE ROLE AS ENUM('Actor', 'Director', 'Producer', 'Writer');

-- ROLE ------------------------------------------------------------
CREATE TABLE personal_role(
    pk SERIAL PRIMARY KEY,
    role ROLE,
    person INTEGER REFERENCES person(pk)
);

-- MOVIE -----------------------------------------------------------
CREATE TABLE movie(
    pk SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    year SMALLINT,
    company VARCHAR(1000),
    budget VARCHAR(50),
    gross VARCHAR(50),
    released VARCHAR(50),
    runtime VARCHAR(50),
    plot TEXT,
    awards TEXT,
    poster VARCHAR(1000),
    website VARCHAR(1000),
    imdb_rating VARCHAR(10),
    imdb_id VARCHAR(50),
    country INTEGER REFERENCES country(pk),
    rating INTEGER REFERENCES rating(pk),
    genre INTEGER REFERENCES genre(pk),
    language INTEGER REFERENCES language(pk)
);

-- INVOLVEMENT -----------------------------------------------------
CREATE TABLE involvement(
    pk SERIAL PRIMARY KEY,
    role ROLE,
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