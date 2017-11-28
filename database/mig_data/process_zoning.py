import pandas as pd
import numpy as np
import json
import re

from database_connection import databaseConnection

def parse_final_zoning_section(x):
    #third part of zoning code designates min lot size or max height
    #if is_digit then indicates number of allowable stories
    lot_size = {
        'A': 3000,
        'B': 4500,
        'C': 5500,
        'D': 6000,
        'E': 7000,
        'F': 8500,
        'G': 9000,
        'H': 10000,
        'I': 12000,
        }

    special_purpose = {
        '1': 'ACCESSORY_DWELLING_UNIT',
        '2': 'ACCESSORY_DWELLING_UNIT_AND_DUPLEX',
        }

    if 'X' in x:
        parsed = ['SPECIAL_PROVISIONS_FOR_ZONE_DISTRICT']
        parsed = []
    else:
        parsed = []

    x = x.strip('+X')
    if x != '2.5':
        x = re.findall('\d+|\D+', x)
    else:
        x = [x]

    alpha_characters = sorted([_ for _ in x if _.isalpha()])
    numeric_characters = set(x).difference(set(alpha_characters))
    matched_alpha_characters = [lot_size.get(_, special_purpose.get(_, None)) for _ in alpha_characters]
    matched_numeric_characters = [special_purpose.get(_, _) for _ in numeric_characters]
    parsed.extend(matched_numeric_characters)
    parsed.extend(matched_alpha_characters)

    #lot_size, accessory, special, stories
    ordered_and_parsed = [np.nan] * 4
    for v in parsed:
        if v in lot_size.values():
            ordered_and_parsed.pop(0)
            ordered_and_parsed.insert(0, v)
        elif v in special_purpose.values():
            ordered_and_parsed.pop(1)
            ordered_and_parsed.insert(1, v)
        elif v == 'SPECIAL_PROVISIONS_FOR_ZONE_DISTRICT':
            ordered_and_parsed.pop(2)
            ordered_and_parsed.insert(2, v)
        else:
            ordered_and_parsed.pop(3)
            ordered_and_parsed.insert(3, v)
    return ordered_and_parsed


def define_zoning(s):
    '''
    INPUT: PANDAS SERIES
        COLUMNS: ['schednum', 'zone']

    '''

    #first letter of zone code
    neighborhood_context = {
        'C': 'URBAN_CENTER',
        'CO': 'OVERLAY_DISTRICT',
        'CMP': 'CAMPUS',
        'D': 'DOWNTOWN',
        'DO': 'OVERLAY_DISTRICT',
        'E': 'URBAN_EDGE',
        'G': 'GENERAL_URBAN',
        'I': 'INDUSTRIAL',
        'M': 'MASTER_PLANNED',
        'OS': 'OPEN_SPACE',
        'S': 'SUBURBAN',
        'U': 'URBAN',
        'UO': 'OVERLAY_DISTRICT',
        }

    #second part of zoning code designates dominant building form and character
    building_form = {
        'CC': 'COMMERCIAL_CHARACTER',
        'MS': 'MAIN_STREET',
        'MU': 'MULTI_UNIT',
        'MX': 'MIXED_USE',
        'RH': 'ROW_HOUSE',
        'RO': 'RESIDENTIAL_OFFICE',
        'RX': 'RESIDENTIAL_MIXED_USE',
        'SU': 'SINGLE_UNIT',
        'TU': 'TWO_UNIT',
        'TH': 'TOWN_HOUSE',
        }

    #only keep zones which are parsable at the moment of the form xx-xx-xx
    s['split_zone'] = s['zone'].str.strip().str.split('-')
    s['is_parseable'] = s['split_zone'].apply(lambda x: len(x) >= 3)
    s = s.copy()[s['is_parseable']]
    c = pd.DataFrame([_ for _ in s['split_zone']], columns=['nbh_context', 'bldg_form', 'other'])
    c['nbh_context'] = c['nbh_context'].replace(neighborhood_context)
    c['bldg_form'] = c['bldg_form'].replace(building_form)

    c['other'] = c['other'].apply(parse_final_zoning_section)
    o = pd.DataFrame([_ for _ in c['other']], columns=['lot_size', 'accessory_type', 'other', 'stories'])

    s.drop([
        'is_parseable',
        'split_zone'
        ], axis=1, inplace=True)
    c.drop('other', axis=1, inplace=True)
    df = pd.DataFrame(np.hstack((s.values, c.values, o.values)), columns=['schednum', 'zone', 'nbh_context', 'bldg_form', 'lot_size', 'accessory', 'other', 'stories'])
    return df

def load_residential_zoning_data():
    df = pd.read_csv('../duplexes/data/real_property_residential_characteristics.csv', dtype='object')
    cols = [col.lower() for col in df.columns.tolist()]
    df.columns = cols
    df.rename(columns={
        'zone10': 'zone',
        }, inplace=True)
    return df[['schednum', 'zone']]

def add_unparseable_zoning_to_zone_df(df, zone_df):
    zone_df = pd.concat([zone_df, df])
    zone_df.drop_duplicates(subset='schednum', keep='first', inplace=True)
    zone_df.reset_index(drop=True, inplace=True)
    return zone_df

def format_dataframe_for_sql_table(df):
    df.rename(columns={
        'zone': 'zoning',
        'nbh_context': 'neighborhood_context',
        'bldg_form': 'building_form',
        'lot_size': 'min_lot_size',
        'accessory': 'accessory_units',
        'other': 'has_special_provisions',
        'stories': 'max_stories',
        'schednum': 'county_identifier',
        }, inplace=True)
    df.fillna('', inplace=True)
    df['min_lot_size'] = df['min_lot_size'].astype(str)
    df['has_special_provisions'].replace({'SPECIAL_PROVISIONS_FOR_ZONE_DISTRICT': True, '': False}, inplace=True)
    df['has_special_provisions'] = df['has_special_provisions'].astype(str)

def output_to_sql_data(df):
    cols_order = ['zoning', 'neighborhood_context', 'building_form', 'min_lot_size', 'accessory_units', 'has_special_provisions', 'max_stories', 'county_identifier']

    with open('prop_zoning_sql_import_formatted.csv', 'w') as f:
        for row in df[cols_order].values.tolist():
            print row[:-1]
            f.write(','.join(row).encode('utf-8') + '\n')

def main():
    df = load_residential_zoning_data()
    zone_df = define_zoning(df.copy())
    zone_df = add_unparseable_zoning_to_zone_df(df, zone_df)
    format_dataframe_for_sql_table(zone_df)
    output_to_sql_data(zone_df)
    return zone_df

if __name__ == '__main__':
    df = main()
