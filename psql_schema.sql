-- make sure the user exists
DO
$body$
BEGIN
  IF NOT EXISTS (
    SELECT *
    FROM pg_catalog.pg_user
    WHERE usename = 'fatchance'
  ) THEN
    CREATE ROLE fatchance LOGIN PASSWORD 'fatchance';
  END IF;
END
$body$
;

-- create the database
CREATE DATABASE fatchance OWNER fatchance;

-- connect to the database we just created
\c fatchance

-- create the user table
BEGIN;
  CREATE TABLE users (
    username text PRIMARY KEY,
    hashpass text
  );
COMMIT;

-- create the weigh-in table
BEGIN;
  CREATE TABLE weighins (
    weighdate date,
    username text REFERENCES users(username),
    weight real,
    PRIMARY KEY (weighdate, username)
  );
COMMIT;

-- grant permissions to fatchance user on the above tables
BEGIN;
GRANT ALL PRIVILEGES ON TABLE users TO fatchance;
GRANT ALL PRIVILEGES ON TABLE weighins TO fatchance;
COMMIT;

-- set up testing users
-- BEGIN;
-- INSERT INTO users VALUES ('admin', 'password');
-- INSERT INTO users VALUES ('zlamberty', 'bigdog13');
-- COMMIT;
