CREATE TABLE jobsite_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    type VARCHAR(50) NOT NULL,
    full_name VARCHAR(50) NULL,
    phone_number VARCHAR(20) NULL,
    education TEXT NULL,
    experience TEXT NULL,
    skills TEXT NULL,
    hobbies TEXT NULL,
    foreign_languages TEXT NULL,
    current_company VARCHAR(50) NULL,
    job_title VARCHAR(100) NULL
);

CREATE TABLE jobsite_company (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    type VARCHAR(50) NOT NULL,
    company_name VARCHAR(50) NULL,
    industry VARCHAR(50) NULL,
    phone_number VARCHAR(20) NULL,
    description TEXT NULL
);


CREATE TABLE jobsite_ad (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    company_name VARCHAR(50) NULL,
    industry VARCHAR(50) NULL,
    department VARCHAR(50) NULL,
    job_type VARCHAR(50) NULL,
    study_level VARCHAR(50) NULL,
    career_level VARCHAR(50) NULL,
    phone_number VARCHAR(20) NULL,
    job_title VARCHAR(100) NULL,
    job_description TEXT NULL,
    job_location VARCHAR(50) NULL,
    salary VARCHAR(20) NULL,
    posted_date DATE NULL,
    
    FOREIGN KEY (company_id) REFERENCES jobsite_company (id)
);

CREATE TABLE jobsite_application(id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,

    FOREIGN KEY (ad_id) REFERENCES jobsite_ad (id)
    FOREIGN KEY (user_id) REFERENCES jobsite_user (id));




SELECT * FROM jobsite_user;

DROP TABLE jobsite_user;

SELECT * FROM jobsite_company;

DROP TABLE jobsite_company;

SELECT * FROM jobsite_ad;

DROP TABLE jobsite_ad;

SELECT * FROM jobsite_application;

DROP TABLE jobsite_application;

INSERT INTO jobsite_user (full_name,email ,password,type)
VALUES( 'admin','ownerlicenta@gmail.com','Admin123','admin');

UPDATE jobsite_user
SET password = 'Admin1234'
WHERE id = 1;
