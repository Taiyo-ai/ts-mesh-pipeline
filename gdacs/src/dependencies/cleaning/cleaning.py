# python
import json

# 3rd
import tldextract
import pandas as pd

# own
from dependencies.utils.utils import (
                                        write_csv_file,
                                        read_json_file,
                                        write_json_file
                                    )


def fix_data():
    """
    Fix data to fill missing fields
    reads from get data file

    write data to a txt file at the end with all the
    missing field except geocode data
    """
    print("Fixing missing fields")
    data = read_json_file('scraped_metadata.json', 'scraped_metadata')

    for item in data:
        subdomain, domain, suffix = tldextract.extract(item['link'])

        item['subdomain'] = subdomain
        item['domain'] = domain + '.' + suffix
        item['aug_id'] = 'GDACS_'+str(item['gdacs:eventid'])
        item['sample_frequency'] = '7 days'
        item['units'] = 'N/A'
        item['source_abbr'] = 'GDACS'
        item['tags'] = [item['gdacs:eventtype'], item['gdacs:alertlevel']]
        item['lonlat'] = [
                           item['geo:Point']['geo:lat'],
                           item['geo:Point']['geo:long']
                         ]
        item['timestamps'] = [item['gdacs:fromdate'], item['gdacs:todate']]

    data = json.dumps(data)

    write_json_file('scraped_main_data.json', 'scraped_main_data', data)


def remove_duplicated(data: pd.DataFrame):
    """
        Remove duplicated rows from the dataframe

        parameters:
            data (DataFrame): dataframe with clean data

        Return:
            data (DataFrame): dataframe without duplicated rows.
    """
    print("Removing duplicated rows")
    return data.loc[data.astype(str).drop_duplicates().index]


def clean_data():
    """
    Remove all innecesary data and writes the file
    Remove duplicated rows
    read from fix data file
    """
    print("Cleaning data")
    data = read_json_file('scraped_main_data.json', 'scraped_main_data')
    cleaned_data = []

    for row in data:
        # row is text, we need translate this to dictionary
        # row = ast.literal_eval(row)
        cleaned_data.append({
            'aug_id': row['aug_id'],
            'gdacs:eventid': row['gdacs:eventid'],
            'sample_frequency': row['sample_frequency'],
            'title': row['title'],
            'description': row['description'],
            'units': row['units'],
            'source_abbr': row['source_abbr'],
            'link': row['link'],
            'domain': row['domain'],
            'subdomain': row['subdomain'],
            'tags': row['tags'],
            'gdacs:country': row['gdacs:country'],
            'gdacs:iso3': row['gdacs:iso3'],
            'timestamps': row['timestamps'],
            'lonlat': row['lonlat'],
            'fromdate': row['gdacs:fromdate']
        })

    cleaned_data = pd.DataFrame.from_dict(cleaned_data)
    cleaned_data = remove_duplicated(cleaned_data)

    write_csv_file('cleaned_main_data.csv', 'cleaned_main_data', cleaned_data)
