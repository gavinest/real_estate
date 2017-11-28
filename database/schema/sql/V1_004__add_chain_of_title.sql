CREATE TABLE transfers (
    id SERIAL PRIMARY KEY,
    location_id UUID REFERENCES locations(id),
    grantee varchar(50) NOT NULL,
    grantor varchar(50) NOT NULL,
    instrument varchar(50) NOT NULL,
    sale_date DATE NOT NULL,
    amount DECIMAL,
    reception_date DATE,
    county_transfer_identifier varchar(50),
    county_identifier VARCHAR(20) NOT NULL
);

