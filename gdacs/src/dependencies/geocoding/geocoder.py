# python
import ast

# 3rd
from geopy.geocoders import GeoNames
import pandas as pd

# own
from dependencies.utils.utils import write_csv_file, read_csv_file, get_world_bank_region_data


def add_geocode_data():
    """
        Read csv with clean data
        Adds geocoded data with given latitude and longitude
        Adds region name and region code as World Bank stadard
        Write csv file with filled data
    """

    print('Adding geocode data')

    dataframe = read_csv_file('cleaned_main_data.csv', 'cleaned_main_data')
    dataframe.drop('Unnamed: 0', inplace=True, axis=1)
    location_values = dataframe.filter(['lonlat', 'gdacs:country', 'gdacs:iso3'])
    # could be an env variable but don't added to make it easy run
    geo = GeoNames(username='challenge_gdacs')

    region = get_region(location_values)
    location = get_geocode_data(geo, location_values)

    dataframe['region_name'] = region['region_name']
    dataframe['region_code'] = region['region_code']
    dataframe['location'] = location['location_data']
    dataframe['state'] = location['state_data']
    dataframe['country'] = location['country_data']
    dataframe['city'] = location['city_data']
    dataframe['locality'] = location['locality_data']
    dataframe['nieghbourhood'] = location['nieghbourhood_data']

    write_csv_file('geocoded_cleaned_data.csv', 'geocoded_cleaned_data', dataframe)


def get_region(dataframe: pd.DataFrame):
    """
        Download and read World Bank standard region names and codes
        Adds region name and code to every row if available

        Parameters:
            dataframe (DataFrame): dataframe with iso3 country code

        Return:
            region_dataframe (list): list with region_name and region code to append to the main dataframe
    """

    print('Adding region name and region code')
    woorkbook = get_world_bank_region_data()

    country_region = pd.read_excel(woorkbook, "List of economies", nrows=219)
    region_codes = pd.read_excel(
        woorkbook,
        "List of economies",
        skiprows=220,
        usecols='A:B',
        header=None
    )

    region_dataframe = {}
    region_name_data = []
    region_code_data = []

    for key, value in dataframe.iterrows():
        if value['gdacs:iso3'] != 'nan':
            country_code = value['gdacs:iso3']
            region_name = country_region.loc[country_region['Code']==country_code]
            if not region_name.empty:
                region_name = region_name.iloc[0]['Region']
                region_code = region_codes.loc[region_codes[0]==region_name]
                region_code = region_code.iloc[0][1]
                region_name_data.append(region_name)
                region_code_data.append(region_code)
            else:
                region_name_data.append('')
                region_code_data.append('')
        else:
            region_name_data.append('')
            region_code_data.append('')

    region_dataframe['region_name'] = region_name_data
    region_dataframe['region_code'] = region_code_data
    return region_dataframe


def get_geocode_data(client, dataframe: pd.DataFrame):
    """
        Gets geocode data from latitude and longitude
        Reads Geonames api (up to 1k free request per day)

        Parameters:
            client (Geonames): geonames client to query rest api
            dataframe (DataFrame): dataframe with longitude and
            latitude available

        Returns:
            general_country (list): List with location, city, state,
            country, locality and neighbourhood to append to the main dataframe
    """

    print('Adding city, country, state, location, etc... \
        from http://www.geonames.org/export/web-services.html')
    general_country = {}
    location_data = []
    city_data = []
    state_data = []
    country_data = []
    locality_data = []
    nieghbourhood_data = []

    for key, value in dataframe.iterrows():
        if value['lonlat'] != 'nan':
            lonlat = ast.literal_eval(value.lonlat)
            latitude = lonlat[0]
            longitude = lonlat[1]
            location = client.reverse(
                query=(latitude, longitude),
                exactly_one=False,
                timeout=5
            )

            if location is not None:
                full_location = location[0].raw
                city = full_location['name']
                state = full_location['adminName1']
                country = full_location['countryName']
                full_location = city + ', ' + state + ', ' + country
            else:
                full_location, city, state, country = '', '', '', ''
        else:
            full_location, city, state, country = '', '', '', ''

        location_data.append(full_location)
        city_data.append(city)
        state_data.append(state)
        country_data.append(country)
        locality_data.append('')
        nieghbourhood_data.append('')

    general_country['location_data'] = location_data
    general_country['city_data'] = city_data
    general_country['state_data'] = state_data
    general_country['country_data'] = country_data
    general_country['locality_data'] = locality_data
    general_country['nieghbourhood_data'] = nieghbourhood_data

    return general_country
