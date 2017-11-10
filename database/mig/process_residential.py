import pandas as pd

from database_connection import databaseConnection

def get_relation_to_locations_table():
    conn = databaseConnection.stage()
    relation_df = pd.read_sql('SELECT id AS location_id, county_identifier FROM locations;', conn, index_col='county_identifier')
    conn.close()
    return relation_df

def insert_into_db(table_name, df):
    print '\nAdding values to table {}.'.format(table_name)
    columns = ', '.join(df.columns.tolist())
    insert_values_format = '%s,' * df.shape[1]
    insert_values_format = insert_values_format.rstrip(',')

    data = [tuple(_) for _ in df.values]

    query = 'INSERT INTO {0} ({1}) VALUES '.format(table_name, columns)
    print query

    conn = databaseConnection.stage()
    with conn.cursor() as curs:
        mogrified_data = ','.join(curs.mogrify('('+ insert_values_format +')', x) for x in data)
        curs.execute(query + mogrified_data)
        conn.commit()
    conn.close()

def make_baths_column(df):
    df['hlf_b'] = df['hlf_b'].astype(float) * 0.5
    df['hlf_b'].fillna(0.0, inplace=True)
    df['baths'] = df['hlf_b'] + df['full_b'].astype(float)
    df.drop([
        'hlf_b',
        'full_b',
        ], axis=1, inplace=True)

def make_above_below_finished_sf_columns(df):
    sf_columns = [
        'above_sf',
        'below_sf',
        'fbsmt_sqft',
        'garden_level_sf',
        ]

    df[sf_columns] = df[sf_columns].astype(float)
    df['finished_sf'] = df['above_sf'] + df['below_sf'] - df['fbsmt_sqft']
    df['below_sf'] = df['below_sf'] + df['garden_level_sf']
    df['has_garden_level'] = df['garden_level_sf'] > 0.0
    df.drop([
        'garden_level_sf',
        'fbsmt_sqft',
        ], axis=1, inplace=True)

def clean_residential_property_data():
    df = pd.read_csv('data/20171015_residential_characteristics.csv', dtype='object')
    cols = [col.lower() for col in df.columns.tolist()]
    df.columns = cols
    df.drop([
        'pin',
        'cd',
        'owner',
        'co_owner',
        'owner_num',
        'owner_dir',
        'owner_st',
        'owner_type',
        'owner_apt',
        'owner_city',
        'owner_state',
        'owner_zip',
        'site_nbr',
        'site_dir',
        'site_name',
        'site_mode',
        'site_more',
        'tax_dist',
        'prop_class',
        'property_class',
        'zone10',
        'd_class_cn',
        'ccyrblt',
        'ccage_rm', #TODO table of remodels/ permits from denver
        'asmt_appr_land',
        'land_sqft',
        'total_value',
        'asdland',
        'assess_value',
        'asmt_taxable',
        'asmt_exempt_amt',
        'style_cn',
        'nbhd_1',
        'nbhd_1_cn',
        'legl_description'
        ], axis=1, inplace=True)

    df.rename(columns= {
        'bed_rms': 'beds',
        'area_abg': 'above_sf',
        'bsmt_area': 'below_sf',
        'ofcard': 'num_bldgs',
        'grd_area': 'garden_level_sf',
        'story': 'stories',
        }, inplace=True)

    int_columns = ['num_bldgs', 'stories', 'units']
    df[int_columns] = df[int_columns].astype(int)

    make_baths_column(df)
    make_above_below_finished_sf_columns(df)

    df.set_index('schednum', inplace=True)
    return df[['beds','baths','stories','units','num_bldgs','above_sf','below_sf','finished_sf','has_garden_level']]

def main():
    df = clean_residential_property_data()
    relation_df = get_relation_to_locations_table()
    insert_df = relation_df.join(df, how='inner')
    insert_df = insert_df.where(pd.notnull(insert_df), None)
    insert_into_db('residential', insert_df)
    return insert_df

if __name__ == '__main__':
    df = main()
