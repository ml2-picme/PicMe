DROP TABLE email_list;
DROP TABLE email_stemming;
DROP TABLE image_results;

CREATE TABLE email_list (
    ID int PRIMARY KEY AUTO_INCREMENT,
    email_path varchar(200) NOT NULL,
    email_from varchar(100) NOT NULL,
    email_to varchar(100) NOT NULL,
    email_subject varchar(200) NOT NULL,
    email_body varchar(500) NOT NULL,
    CONSTRAINT c_unique_entry UNIQUE (email_path, email_from, email_to, email_subject, email_body)
);

CREATE TABLE email_stemming (
    ID int PRIMARY KEY AUTO_INCREMENT,
    emailID int NOT NULL,
    stemming_word varchar(100) NOT NULL,
    FOREIGN KEY (emailID) REFERENCES email_list(ID),
    CONSTRAINT c_unique_stemming UNIQUE (emailID, stemming_word)
);

CREATE TABLE image_results(
    local_path varchar(250) NOT NULL,
    model varchar(100) NOT NULL,
    prediction_class varchar(100) NOT NULL,
    prediction_class_stemmed varchar(100) NOT NULL,
    prediction_probability float NOT NULL,
    PRIMARY KEY(local_path,model,prediction_class,prediction_probability)
);
