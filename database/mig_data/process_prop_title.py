import pandas as pd
import numpy as np
import json

def load_data():
    with open('scrape_data/20171026_den_tax_scrape/prop_title.txt', 'r') as f:
        data = []
        for line in f.readlines():
            data.append(json.loads(line.strip('\n')))
    return data

def load_pins_to_schednum():
    df = pd.read_csv('data/20171015_residential_characteristics.csv', dtype='object')
    df = df[['PIN', 'SCHEDNUM']]
    df.columns = ['pin', 'schednum']
    # df.set_index('schednum', inplace=True)
    return df

def clean_title_data(data):
    formatted_dataframes = []
    for prop in data:
        try:
            pin, prop_title_history = prop.values()
        except ValueError:
            print '\nError. No transfer data for pin {}'.format(prop['pin'])
            continue
        else:
            temp_df = pd.DataFrame(prop_title_history)
            temp_df['pin'] = pin
            formatted_dataframes.append(temp_df)
    df = pd.concat(formatted_dataframes)
    return df

def format_dataframe_for_sql_table(df):
    cols = ['_'.join(_.lower().split(' ')) for _ in df.columns.tolist()]
    df.columns = cols
    # df['sale_date'] = pd.to_datetime(df['sale_date']).dt.strftime('%Y-%m-%d')
    # df['reception_date'] = pd.to_datetime(df['reception_date']).dt.strftime('%Y-%m-%d')
    df['sale_date'] = df['sale_date'].apply(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d') if len(x.split('-', 1)[0]) == 4 else x)
    df['reception_date'] = df['reception_date'].apply(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d') if len(x.split('-', 1)[0]) == 4 else x)
    df.rename(columns={
        'sale_price': 'amount',
        'reception_number': 'county_transfer_identifier',
        'schednum': 'county_identifier'
        }, inplace=True)
    df['amount'] = df['amount'].apply(lambda x: ''.join(x.strip('$').split(',')))
    for char in ',"':
        df['grantee'].replace(char, value='', regex=True, inplace=True)
        df['grantor'].replace(char, value='', regex=True, inplace=True)

def output_to_sql_data(df):
    cols_order = ['grantee', 'grantor', 'instrument', 'sale_date', 'amount', 'reception_date', 'county_transfer_identifier', 'county_identifier']

    with open('prop_title_sql_import_formatted.csv', 'w') as f:
        for row in df[cols_order].values.tolist():
            f.write(','.join(row).encode('utf-8') + '\n')

def main():
    data = load_data()
    df = clean_title_data(data)
    pins_to_schednum_df = load_pins_to_schednum()
    df = pd.merge(df, pins_to_schednum_df, how='left', left_on='pin', right_on='pin')
    format_dataframe_for_sql_table(df)
    output_to_sql_data(df)
    return df

if __name__ == '__main__':
    df = main()
    # d = load_data()
    # a = load_pins_to_schednum()
