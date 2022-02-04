# Thrid package
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy.geocoders import Nominatim
import pandas as pd

# Property packages
from dependencies.utils.utils import read_json_file, save_json_file


def get_geodecoded_data():
    """
        Read json file for cleaned data and save data
    """

    json_file = read_json_file('cleaned_main_data', 'cleaned_main_data.json')
    df = pd.DataFrame.from_dict(json_file, orient='index')
    df_geodecoded = add_geodecoded_data(df)

    # Convert dataframe to json
    json_data = df_geodecoded.to_json(orient='index')

    save_json_file(json_data, 'geocoded_main_data', 'geocoded_main_data.json')

    return None


def add_geodecoded_data(df: pd.DataFrame):
    """
        Add geodecoded data in dataframe
    """

    geolocator = Nominatim(user_agent="ts_mesh_gdelt")

    for index, row in df.iterrows():
        data = get_raw_geocode_dat(row['country_name'], geolocator)

        df.loc[index, ['state']] = data.get('state')
        df.loc[index, ['county']] = data.get('county')
        df.loc[index, ['city']] = data.get('city')
        df.loc[index, ['locality']] = data.get('locality')
        df.loc[index, ['nieghbourhood']] = data.get('nieghbourhood')
        df.loc[index, ['location']] = data.get('location')
        df.loc[index, ['latitude']] = data.get('latitude')
        df.loc[index, ['longitude']] = data.get('longitude')

    return df


def get_raw_geocode_dat(country_name: str, geolocator):
    """
        Get raw data and return a dictionary
    """

    latitude = ''
    longitude = ''
    state = country_name
    country = ''
    city = ''
    locality = ''
    nieghbourhood = ''

    try:
        data = geolocator.geocode(country_name).raw

        if bool(data):
            latitude = data['lat']
            longitude = data['lon']
            state = country_name
            country = data['display_name']
            city = data['display_name']
            nieghbourhood = ''

        geocoded_dict = {
            'latitude': latitude,
            'longitude': longitude,
            'state': state,
            'country': country,
            'city': city,
            'locality': locality,
            'nieghbourhood': nieghbourhood,
        }

        return geocoded_dict

    except GeocoderTimedOut:
        return get_raw_geocode_dat(country_name, geolocator)

    except GeocoderUnavailable:
        geocoded_dict = {
            'latitude': latitude,
            'longitude': longitude,
            'state': state,
            'country': country,
            'city': city,
            'locality': locality,
            'nieghbourhood': nieghbourhood,
        }

        return geocoded_dict
