CREATE DATABASE IF NOT EXISTS ml2;

DROP TABLE IF EXISTS ml2.email_stemming;
DROP TABLE IF EXISTS ml2.email_list;
DROP TABLE IF EXISTS ml2.image_stemming;
DROP TABLE IF EXISTS ml2.image_list;

CREATE TABLE IF NOT EXISTS ml2.email_list (
    ID int PRIMARY KEY AUTO_INCREMENT,
    email_path varchar(200) NOT NULL,
    email_from varchar(100) NOT NULL,
    email_to varchar(100) NOT NULL,
    email_subject varchar(200) NOT NULL,
    email_body varchar(500) NOT NULL,
    CONSTRAINT c_email_list UNIQUE (email_path, email_from, email_to, email_subject, email_body)
);

CREATE TABLE IF NOT EXISTS ml2.email_stemming (
    ID int PRIMARY KEY AUTO_INCREMENT,
    emailID int NOT NULL,
    stemming_word varchar(100) NOT NULL,
    FOREIGN KEY (emailID) REFERENCES email_list(ID) ON DELETE CASCADE,
    CONSTRAINT c_email_stemming UNIQUE (emailID, stemming_word)
);

CREATE TABLE IF NOT EXISTS ml2.image_list (
  ID int PRIMARY KEY AUTO_INCREMENT,
  local_path varchar(250) NOT NULL,
  model varchar(100) NOT NULL,
  prediction_class varchar(100) NOT NULL,
  prediction_probability float NOT NULL,
  CONSTRAINT c_image_list UNIQUE (local_path, model, prediction_class, prediction_probability)
);

CREATE TABLE IF NOT EXISTS ml2.image_stemming (
  ID int PRIMARY KEY AUTO_INCREMENT,
  imageID int NOT NULL,
  stemming_word varchar(100) NOT NULL,
  FOREIGN KEY (imageID) REFERENCES image_list(ID) ON DELETE CASCADE,
  CONSTRAINT c_image_stemming UNIQUE (imageID, stemming_word)
);
