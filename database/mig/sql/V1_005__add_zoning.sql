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
