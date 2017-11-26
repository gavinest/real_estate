CREATE TABLE taxes (
    id SERIAL PRIMARY KEY,
    year SMALLINT NOT NULL,
    tax_amount DECIMAL NOT NULL,
    imp_area INTEGER
);
