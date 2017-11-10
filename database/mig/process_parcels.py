import pandas as pd
import numpy as np
import re

from database_connection import databaseConnection
from scrape_data import property_use_id_clean

def correct_property_use_id(df):
    original_use_ids = property_use_id_clean.original_use_ids()
    original_use_df = pd.DataFrame(original_use_ids, columns=['original_use_id', 'use_type'], dtype='object')
    unique_use_ids = property_use_id_clean.unique_use_ids()
    unique_use_df = pd.DataFrame(unique_use_ids, columns=['property_use_id', 'use_type'], dtype='object')
    temp_df = pd.merge(original_use_df, unique_use_df, left_on='use_type', right_on='use_type')

    df['property_use_id'].fillna(-9999, inplace=True)
    df['property_use_id'] = df['property_use_id'].astype(int)
    corrected_use_df = pd.merge(df, temp_df, how='left', left_on='property_use_id', right_on='original_use_id')

    corrected_use_df.drop([
        'property_use_id_x',
        'original_use_id',
        'use_type'
        ],axis=1, inplace=True)

    corrected_use_df.rename(columns={'property_use_id_y': 'property_use_id'}, inplace=True)
    return corrected_use_df

def format_data_types(df):
    int_columns = [
        'zip',
        'county_id',
        'land_sf',
        'yr_built',
        'property_class_id',
        'property_use_id'
        ]
    df = df.where(pd.notnull(df), -9999)
    df[int_columns] = df[int_columns].astype(np.int64)
    df.replace({-9999: None}, inplace=True)
    return df

def insert_into_db(table_name, df):
    print '\nAdding values to table {}.'.format(table_name)
    columns = ', '.join(df.columns.tolist())
    insert_values_format = '%s,' * df.shape[1]
    insert_values_format = insert_values_format.rstrip(',')

    df = format_data_types(df)
    data = [tuple(_) for _ in df.values]

    query = 'INSERT INTO {0} ({1}) VALUES '.format(table_name, columns)
    print query

    conn = databaseConnection.stage()
    with conn.cursor() as curs:
        mogrified_data = ','.join(curs.mogrify('('+insert_values_format+')', x) for x in data)
        curs.execute(query + mogrified_data)
        conn.commit()
    conn.close()

def clean_zip_code(series):
    series = series.apply(lambda x: x.split('-')[0] if type(x) != float else x)
    series = series.str.strip('CO ')
    series.replace({'': np.nan}, inplace=True)
    series = series.apply(lambda x: re.sub('[^0-9]', '', x) if type(x) == str else x)
    return series

def create_class_ids(df):
    unique_classes = df['class_description'].drop_duplicates()
    unique_classes.dropna(inplace=True)
    unique_classes.reset_index(drop=True, inplace=True)
    class_ids = pd.Series(np.arange(1, unique_classes.shape[0] + 1, step=1))
    class_ids.name = 'property_class_id'
    class_xref = pd.concat([class_ids, unique_classes], axis=1)
    class_xref['property_class_id'] = class_xref['property_class_id'].astype('object')
    return class_xref

def prepare_parcel_data():
    df = pd.read_csv('data/20171013_parcels.csv', dtype='object')
    cols = [col.lower() for col in df.columns.tolist()]
    df.columns = cols

    # 'schednum',
    # 'land',
    # 'd_class', #TODO pick list of class code defined 'd_class_cn'
    # 'dcl12',
    # 'act_zone',
    # 'imp_area',
    # 'ccyrblt',

    #drop unneccesary columns off the bat
    df.drop([
        'pin',
        'mapnum',
        'blknum',
        'parcelnum',
        'appendage',
        'parcel_source',
        'system_start_date',
        'owner_name',
        'owner_address_line1',
        'owner_address_line2',
        'owner_addr_nbr_prefix',
        'owner_addr_nbr',
        'owner_addr_nbr_suffix',
        'owner_str_name_pre_mod',
        'owner_str_name_pre_dir',
        'owner_str_name_pre_type',
        'owner_str_name',
        'owner_str_name_post_type',
        'owner_str_name_post_dir',
        'owner_str_name_post_mod',
        'owner_unit_type',
        'owner_unit_ident',
        'owner_city',
        'owner_state',
        'owner_zip',
        'tax_dist',
        'land_value',
        'improvement_value',
        'improvements',
        'total_value',
        # 'd_class_cn',
        'd_class',
        'asal_instr',
        'sale_monthday',
        'sale_year',
        'sale_price',
        'reception_num',
        'situs_address_id',
        'situs_address_line2',
        'situs_addr_nbr',
        'situs_addr_nbr_suffix',
        'situs_str_name_pre_mod',
        'situs_str_name_pre_dir',
        'situs_str_name_pre_type',
        'situs_str_name',
        'situs_str_name_post_type',
        'situs_str_name_post_dir',
        'situs_str_name_post_mod',
        'situs_state',
        'situs_unit_type',
        'situs_unit_ident',
        'prop_class', #TODO pick list for property class codes (used in tax table since this code is used for denver taxation)
        'imp_area', #TODO save column for taxes
        ],axis=1, inplace=True)

    #rename columns that are keeping
    rename_cols = {
        'ccyrblt': 'yr_built',
        'schednum': 'county_identifier',
        'dcl12': 'property_use_id',
        # 'd_class': 'property_class_id',
        'land': 'land_sf',
        'situs_address_line1': 'address',
        'situs_city': 'city',
        'situs_zip': 'zip',
        'act_zone': 'zoning',
        'd_class_cn': 'class_description',
        }
    df.rename(columns=rename_cols, inplace=True)

    df['zip'] = clean_zip_code(df['zip'])
    df['yr_built'].replace({'0': np.nan}, inplace=True)
    df['zoning'] = df['zoning'].str.strip()
    df['county_id'] = '2'
    df['state'] = 'CO'
    df = correct_property_use_id(df)
    return df

def main():
    df = prepare_parcel_data()
    class_xref = create_class_ids(df)
    df = pd.merge(df, class_xref, how='left', left_on='class_description', right_on='class_description')
    df.drop('class_description', axis=1, inplace=True)
    df = format_data_types(df)
    insert_into_db('locations', df)
    return df[['county_identifier','address','city','state','zip','county_id','yr_built','land_sf','zoning','property_class_id', 'property_use_id']]

if __name__ == "__main__":
    # df = prepare_parcel_data()
    df = main()
    # insert_into_db('locations', pd.DataFrame())
    # u, o =  correct_property_use_id(pd.DataFrame())
