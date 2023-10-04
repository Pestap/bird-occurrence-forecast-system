CREATE DATABASE observations_db;

USE observations_db;

CREATE TABLE observations (
    common_name varchar(255),
    scientific_name varchar(255),
    observation_count float,
    country varchar(255),
    state_name varchar(255),
    state_code varchar(255),
    latitude float,
    longitude float
)