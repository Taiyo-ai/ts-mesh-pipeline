import os
import pandas as pd
import country_converter as coco
import pycountry
import math
from datetime import datetime

DATA_DIR = '../scraping/weather_forecast.csv'


class Cleaner:

    def __init__(self):
        return None

    def load_data(self):
        """load csv data from the directory"""

        df = pd.read_csv(DATA_DIR)
        return df

    def remove_duplicates(self, df):
        """remove duplicates row in the datframe"""

        df.drop_duplicates(keep='first', inplace=True)
        return df

    def check_missing_values(self, df):
        """check for missing values replace it with NaN"""
        df.replace(' ', math.nan)
        return df

    def country_iso_code(self, df):
        """convert country codes to ISO 3166-1 alpha3"""

        df['country'] = df['country'].apply(lambda x: pycountry.countries.get(
            alpha_2=x).alpha_3 if (len(x) == 2) else pycountry.countries.get(name=x).alpha_3)
        return df

    def convert_timestamp(self, df):
        """convert UNIX timestamp to %Y-%m-%d %H:%M:%S format"""

        df['dt'] = df['dt'].apply(lambda x: datetime.utcfromtimestamp(
            int(x)).strftime('%Y-%m-%d %H:%M:%S'))
        return df

    def rename_columns(self, df):
        """rename columns of dataframe"""
        pass

    def get_region_name(self, df):
        """get region name using the country code"""

        df['region_name'] = df['country'].apply(
            lambda x: pycountry.countries.get(alpha_3=x).name)
        return df

    def get_region_code(self, df):
        """get region code using the country code"""

        df['region_code'] = df['country'].apply(
            lambda x: pycountry.countries.get(alpha_3=x).numeric)
        return df

    def create_timeseries_data(self, df):
        """create time series data from the cleaned data"""

        timeseries_columns = ['id', 'humidity', 'pressure', 'wind_speed', 'temp.average',
                              'temp.average_max', 'temp.average_min', 'temp.record_max', 'temp.record_min']
        df_timeseries = df[timeseries_columns]

        return df_timeseries

    def save_data(self, df, filename):
        """save the cleaned dataframe"""

        df.to_csv(filename)
        return df

    def run(self):
        """perform cleaning operation the raw data"""

        print('Cleaning process started...')
        df = self.load_data()
        self.remove_duplicates(df)
        self.check_missing_values(df)
        df = self.convert_timestamp(df)
        df = self.country_iso_code(df)
        df = self.get_region_name(df)
        df = self.get_region_code(df)
        df = self.save_data(df, filename='cleaned_data.csv')
        df_timeseries = self.create_timeseries_data(df)
        df_timeseries = self.save_data(df_timeseries, filename='timeseries_data.csv')
        print('Cleaning process finished.')

        return df


if __name__ == "__main__":
    config = {}
    myCleaner = Cleaner()
    mydf = myCleaner.run()
