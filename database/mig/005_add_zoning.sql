CREATE TABLE zoning (
    id SERIAL PRIMARY KEY,
    location_id UUID REFERENCES locations(id),
    zoning VARCHAR(30) NOT NULL,
    neighborhood_context VARCHAR(30),
    building_form VARCHAR(30),
    min_lot_size VARCHAR(20),
    accessory_units VARCHAR(50),
    has_special_provisions BOOLEAN,
    max_stories NUMERIC,
    county_identifier VARCHAR(50)
);

COPY zoning (zoning, neighborhood_context, building_form, min_lot_size, accessory_units, has_special_provisions, max_stories, county_identifier) FROM '/Users/Gavin/projects/re/database/prop_zoning_sql_import_formatted.csv' DELIMITER ',' CSV;

UPDATE zoning SET location_id=locations.id FROM locations WHERE zoning.county_identifier=locations.county_identifier;

ALTER TABLE zoning DROP county_identifier;
