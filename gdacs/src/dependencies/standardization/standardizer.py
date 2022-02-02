# Python
import datetime

# own
from dependencies.utils.utils import write_csv_file, read_csv_file

# 3rd
import pandas as pd


class Event:
    """
        Event class
    """
    def __init__(
        self,
        aug_id: str,
        original_id: int,
        sample_frequency: str,
        name: str,
        description: str,
        units: str,
        source: str,
        url: str,
        domain: str,
        subdomain: str,
        tags: list,
        country_name: str,
        country_code: str,
        region_name: str,
        region_code: str,
        state: str,
        country: str,
        city: str,
        locality: str,
        nieghbourhood: str,
        location: str,
        map_coordinates: list,
        timestamps: list
    ):
        """
        Holds standarized data from every event

        Args:
            aug_id: ID generated for unique identification
            original_id: ID originally provided by the data source
            sample_frequency: sample frequency of the time_series
            name: Name or Title of the time series
            description:  Any descriptive information present about the timeseries
            units: the units of measurement of the timeseries
            source: Source Abbr.
            url: Link to the microsite of the timeseries
            domain: domain of the data source
            subdomain: subdomain of the data source
            tags: Important keywords identified from overall textual content 
            present about the asset
            country_name: The short country name
            country_code: ISO 3166-1 alpha-3 country codes
            region_name:
            region_code: 3 ISO format
            state: State Name
            county: County/District Name
            city: City Name
            locality: Nearest locality
            nieghbourhood:
            location: The exact or approx. location
            map_coordinates: Geographical Coordinates in decimal degree system
            timestamps: start date, end date of the timeseries as a dictionary 
            type

        """

        self.aug_id = aug_id
        self.original_id = original_id
        self.sample_frequency = sample_frequency
        self.name = name
        self.description = description
        self.units = units
        self.source = source
        self.url = url
        self.domain = domain
        self.subdomain = subdomain
        self.tags = tags
        self.country_name = country_name
        self.country_code = country_code
        self.region_name = region_name
        self.region_code = region_code
        self.state = state
        self.country = country
        self.city = city
        self.locality = locality
        self.nieghbourhood = nieghbourhood
        self.location = location
        self.map_coordinates = map_coordinates
        self.timestamps = timestamps

        def __str__(self):
            """
                Returns the string callable method of the class
            """
            return self.name


def rename_columns(dataframe: pd.DataFrame):
    """
        Rename the columns with the correct stadardized name

        Parameters:
            dataframe (Dataframe)

        Returns:
            dataframe (Dataframe)
    """
    print("renaming columns")
    dataframe.rename(
        columns={
            'gdacs:eventid': 'original_id',
            'title': 'name',
            'source_abbr': 'source',
            'link': 'url',
            'gdacs:country': 'country_name',
            'gdacs:iso3': 'country_code',
            'lonlat': 'map_coordinates'
            },
        inplace=True
        )

    return dataframe


def rearranging_columns(dataframe: pd.DataFrame):
    """
        Orders the columns to match given spreadsheet

        Parameters:
            dataframe (Dataframe)

        Returns:
            dataframe (Dataframe)
    """

    print("ordering columns")
    dataframe = dataframe[[ 'aug_id',
                            'original_id',
                            'sample_frequency',
                            'name',
                            'description',
                            'units',
                            'source',
                            'url',
                            'domain',
                            'subdomain',
                            'tags',
                            'country_name',
                            'country_code',
                            'region_name',
                            'region_code',
                            'state',
                            'country',
                            'city',
                            'locality',
                            'nieghbourhood',
                            'location',
                            'map_coordinates',
                            'timestamps']]
    return dataframe


def order_rows_by_ts(dataframe: pd.DataFrame):
    """
        Returns the dataset sorted by start date of the event
    """
    print("sorting rows by date")
    return dataframe.sort_values(by='fromdate', ascending=False)


def standarized_data():
    """
        Check all rows has the correct datatype with the Event class
        Read csv with geocoded cleaned data
        Rename all columns with the correct name
        Order all columns according to the given spreadsheet
        Filter records to match India events
        Write csv with the filtered records except if there isn't recent events, in that case
        writes all the events standardized

    """

    print("making data standardized")
    dataframe = read_csv_file('geocoded_cleaned_data.csv', 'geocoded_cleaned_data')
    dataframe.drop('Unnamed: 0', inplace=True, axis=1)

    dataframe = order_rows_by_ts(dataframe)
    dataframe = rename_columns(dataframe)
    dataframe = rearranging_columns(dataframe)

    # standarized data
    events = [Event(**kwargs) for kwargs in dataframe.to_dict(orient='records')]
    # print(events[0].timestamps)

    final_dataframe = dataframe[dataframe['country_code']=='IND']
    if final_dataframe.empty:
        print("There isn't recent events in India, all other events are saved in csv")
        write_csv_file('standardized_geocoded_data.csv', 'standardized_geocoded_data', dataframe)
    else:
        write_csv_file('standardized_geocoded_data.csv', 'standardized_geocoded_data', final_dataframe)
