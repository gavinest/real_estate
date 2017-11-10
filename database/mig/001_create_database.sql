CREATE DATABASE re;
\c re;

CREATE EXTENSION pgcrypto;

CREATE TABLE locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    county_identifier VARCHAR(20) NOT NULL,
    address varchar(100),
    city VARCHAR(20),
    state VARCHAR(20) NOT NULL,
    zip INTEGER,
    county_id INTEGER NOT NULL,
    yr_built INTEGER,
    land_sf INTEGER,
    zoning VARCHAR(20),
    property_use_id INTEGER,
    property_class_id INTEGER
);
