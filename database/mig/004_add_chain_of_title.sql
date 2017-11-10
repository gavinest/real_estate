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

COPY transfers (grantee, grantor, instrument, sale_date, amount, reception_date, county_transfer_identifier, county_identifier) FROM '/Users/Gavin/projects/re/database/prop_title_sql_import_formatted.csv' DELIMITER ',' CSV;

UPDATE transfers SET location_id=locations.id FROM locations WHERE transfers.county_identifier=locations.county_identifier;

ALTER TABLE transfers DROP county_identifier;
