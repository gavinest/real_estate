CREATE TABLE owners (
	id SERIAL PRIMARY KEY,
	location_id UUID REFERENCES locations(id),	
	owner_string VARCHAR NOT NULL,
	county_identifier VARCHAR(20) NOT NULL
);
