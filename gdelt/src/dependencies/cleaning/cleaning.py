# Third Packages
import tldextract
import pandas as pd
import pycountry
import pycountry_convert as pc

# Property packages
from dependencies.utils.utils import read_json_file, save_json_file


def clean_data():
    """
        Clean data and save the json file in a specific folder.
    """

    df = add_missing_data()
    df_with_country_data = add_country_data(df)
    cleaned_data = []

    for index, row in df_with_country_data.iterrows():
        country_alpha2 = pc.country_alpha3_to_country_alpha2(
            row['country_code']
        )
        country_continent_code = pc.country_alpha2_to_continent_code(
            country_alpha2
        )
        country_continent_name = pc.convert_continent_code_to_continent_name(
            country_continent_code
        )

        cleaned_data.append({
            'aug_id': row['aug_id'],
            'original_id': index,
            'sample_frequency': row['sample_frequency'],
            'name': row['title'],
            'description': row['title'],
            'units': row['units'],
            'source': row['domain'],
            'url': row['url'],
            'domain': row['domain'],
            'subdomain': row['subdomain'],
            'tags': [
                row['language'],
                row['socialimage'],
            ],
            'country_name': row['country_name'],
            'country_code': row['country_code'],
            'region_name': country_continent_name,
            'region_code': country_continent_code,
            'state': '',
            'county': '',
            'city': '',
            'locality': '',
            'nieghbourhood': '',
            'location': '',
            'map_coordinates': '',
            'latitude': '',
            'longitude': '',
            'timestamps': [
                row['seendate'],
                row['seendate'],
            ],
        })

    cleaned_df = pd.DataFrame.from_dict(cleaned_data)
    cleaned_df_without_duplicates = clear_duplicated_rows(cleaned_df)

    # Convert dataframe to json
    json_data = cleaned_df_without_duplicates.to_json(orient='index')

    save_json_file(json_data, 'cleaned_main_data', 'cleaned_main_data.json')

    return None


def add_missing_data():
    """
        Add missing data to create a cleand dataframe
    """

    json_file = read_json_file('scraped_main_data', 'scraped_main_data.json')
    df = pd.DataFrame.from_dict(json_file, orient='index')

    for index, row in df.iterrows():
        subdomain, domain, suffix = tldextract.extract(row['url'])

        df.loc[index, ['aug_id']] = 'GDELT_' + str(index)
        df.loc[index, ['subdomain']] = subdomain
        df.loc[index, ['domain']] = domain + '.' + suffix
        df.loc[index, ['sample_frequency']] = '7 days'
        df.loc[index, ['units']] = 'N/A'
        df.loc[index, ['source_abbr']] = 'GDELT'

    return df


def get_country(country_name: str):
    """
        Get country for a specific country_name
    """

    data_country = pycountry.countries.get(name=country_name)

    if not data_country:
        data_country = pycountry.countries.search_fuzzy(country_name)[0]

    return data_country


def add_country_data(df: pd.DataFrame):
    """
        Add country data.
    """

    df['country_name'] = df['sourcecountry'].apply(
        lambda x: get_country(x).name
    )

    df['country_code'] = df['sourcecountry'].apply(
        lambda x: get_country(x).alpha_3
    )

    return df


def clear_duplicated_rows(df: pd.DataFrame):
    """
        Clear duplicated data
    """

    return df.loc[df.astype(str).drop_duplicates().index]
