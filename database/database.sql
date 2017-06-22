DROP TABLE IF EXISTS Users;

CREATE TABLE Users
  (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name      VARCHAR(40) NOT NULL,
    email     VARCHAR(100) NOT NULL,
    password  BLOB NOT NULL,
    salt      VARCHAR(16) NOT NULL
  );
