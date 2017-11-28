# 004_crate_transfers_table
COPY transfers (grantee, grantor, instrument, sale_date, amount, reception_date, county_transfer_identifier, county_identifier) FROM '/Users/Gavin/projects/re/database/prop_title_sql_import_formatted.csv' DELIMITER ',' CSV;

UPDATE transfers SET location_id=locations.id FROM locations WHERE transfers.county_identifier=locations.county_identifier;

ALTER TABLE transfers DROP county_identifier;

#add zoning data
COPY zoning (zoning, neighborhood_context, building_form, min_lot_size, accessory_units, has_special_provisions, max_stories, county_identifier) FROM '/Users/Gavin/projects/re/database/prop_zoning_sql_import_formatted.csv' DELIMITER ',' CSV;

UPDATE zoning SET location_id=locations.id FROM locations WHERE zoning.county_identifier=locations.county_identifier;

ALTER TABLE zoning DROP county_identifier;

