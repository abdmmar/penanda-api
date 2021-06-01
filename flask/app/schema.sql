DROP DATABASE IF EXISTS bookmark
CREATE DATABASE bookmark

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS bookmark;

CREATE TABLE user (
  id VARCHAR(50) PRIMARY KEY,
  email VARCHAR(100) NOT NULL,
  name VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL
);

CREATE TABLE bookmark (
  id VARCHAR(50) PRIMARY KEY,
  author_id VARCHAR(50) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title VARCHAR(255) NOT NULL,
  url VARCHAR(255) NOT NULL,
  img VARCHAR(255) NULL,
  description VARCHAR(255) NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);