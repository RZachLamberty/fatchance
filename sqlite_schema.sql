drop table if exists weighin_users;
create table weighin_users (
  username text primary key,
  password text not null
);

drop table if exists weighins;
create table weighins (
  username text,
  weighdate text,
  weight real,
  foreign key(username) REFERENCES weighin_users(username),
  primary key (weighdate, username)
);
