CREATE TABLE jobsite_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    type VARCHAR(50) NOT NULL
);

SELECT * FROM jobsite_user;

DROP TABLE jobsite_user;


INSERT INTO jobsite_user (full_name,email ,password,type)
VALUES( 'admin','ownerlicenta@gmail.com','admin123','admin');
