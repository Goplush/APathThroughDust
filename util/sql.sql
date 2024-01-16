CREATE DATABASE `APathThroughTheDust`;

USE `APathThroughTheDust`;


CREATE TABLE `ChainUser` (
  `nickname` VARCHAR(50),
  `rsa_public_key` VARCHAR(3000),
  `registration_time` DATE,
  `user_type` INT,
  `valid_time` INT,
  PRIMARY KEY (nickname)
);


CREATE TABLE UserRealName (
  nickname VARCHAR(50),
  real_name VARCHAR(50),
  hash_value VARCHAR (2000),
  FOREIGN KEY (nickname) REFERENCES ChainUser(nickname) ON DELETE CASCADE
);


CREATE TABLE travel (
    creator CHAR(20) NOT NULL,
    participant CHAR(20) NOT NULL,
    destination VARCHAR(100) not null
    start_date CHAR(10) NOT NULL,
    end_date CHAR(10) NOT NULL,
    necessary_num INT NOT NULL,
    PRIMARY KEY (participant, start_date, end_date)
);

CREATE TABLE Necessaries (
    participant CHAR(15) NOT NULL,
    start_time CHAR(15) NOT NULL,
    end_time CHAR(15) NOT NULL,
    required_participant CHAR(15) NOT NULL,
    description VARCHAR(50),
    event_index INT NOT NULL,
    event_h INT,
    event_i INT,
    PRIMARY KEY (participant, start_time, end_time, event_index)
);



CREATE USER 'DustAdmin'@'%' IDENTIFIED BY 'qMfH8eyH5QLRddGr';


