CREATE TABLE taxes (
    id SERIAL PRIMARY KEY,
    year SMALLINT NOT NULL,
    tax_amount DECIMAL NOT NULL,
    imp_area INTEGER,

);

CREATE TABLE property_class (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);
