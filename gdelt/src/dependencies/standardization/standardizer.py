# Third packages
import pandas as pd

# Property packages
from dependencies.utils.utils import save_json_file, read_json_file


def standardize_data():
    """
        Read geocoded data and process de data and save data into a json file
    """

    json_file = read_json_file('geocoded_main_data', 'geocoded_main_data.json')
    df = pd.DataFrame.from_dict(json_file, orient='index')
    df_standard = standard_dataframe(df)

    # Convert dataframe to json
    json_data = df_standard.to_json(orient='index')

    save_json_file(
        json_data,
        'standardized_main_data',
        'standardized_main_data.json'
    )

    return None


def standard_dataframe(df: pd.DataFrame):
    """
        Create standar dataframe
    """

    standard_data = []

    for index, row in df.iterrows():
        standard_data.append({
            'aug_id': row['aug_id'],
            'original_id': row['original_id'],
            'sample_frequency': row['sample_frequency'],
            'name': row['name'],
            'description': row['description'],
            'units': row['units'],
            'source': row['domain'],
            'url': row['url'],
            'domain': row['domain'],
            'subdomain': row['subdomain'],
            'tags': row['tags'],
            'country_name': row['country_name'],
            'country_code': row['country_code'],
            'region_name': row['region_name'],
            'region_code': row['region_code'],
            'state': row['state'],
            'county': row['county'],
            'city': row['city'],
            'locality': row['locality'],
            'nieghbourhood': row['nieghbourhood'],
            'location': row['location'],
            'map_coordinates': [
                row['latitude'],
                row['longitude']
            ],
            'timestamps': row['timestamps']
        })

    standard_df = pd.DataFrame.from_dict(standard_data)

    return standard_df
