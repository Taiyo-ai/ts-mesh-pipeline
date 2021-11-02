import requests
from datetime import datetime
import pandas as pd
from pandas import json_normalize
import os
import time

url = "https://community-open-weather-map.p.rapidapi.com/climate/month"
FILE_PATH = '../../cities.txt'


class Scrapper:
    def __init__(self):
        return None

    def api_request(self, url, city):
        """fetch 30 days weather forecasts for a city around the world"""

        querystring = {"q": city}
        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': "0853b11a2dmsh562d6f9daefc256p1cfc7fjsn7a0dfc4cf285"
        }
        try:
            response = requests.request(
                "GET", url, headers=headers, params=querystring)
        except:
            #print('Info not availavle for the {}'.format(city))
            pass

        if response.status_code == 429:
            print('Too many requests...trying again after 30 seconds ')
            time.sleep(30)
            response = self.api_request(url, city)

        return response

    def create_df(self, response):
        """create dataframe from the json"""

        if response.status_code == 200:

            json_ = response.json()
            _id = json_['city']['id']
            city = json_['city']['name']
            country = json_['city']['country']

            df1 = pd.DataFrame(
                {'id': [_id], 'city': [city], 'country': [country]})
            df2 = json_normalize(json_['list'])
            df = pd.concat([df1, df2], axis=1)

            df['id'].fillna(_id, inplace=True)
            df['id'] = df['id'] + df['dt'].apply(lambda x : int(str(x)[-7:])) #create a unique id for each row
            df['city'].fillna(city, inplace=True)
            df['country'].fillna(country, inplace=True)

        else:
            print(response.status_code)
            df = pd.DataFrame()

        return df

    def save_df(self, df):
        """save dataframe"""
        df.to_csv('weather_forecast.csv')

    def run(self):
        """create the raw data"""
        df = pd.DataFrame()

        print('Scrapping operations started...')
        start = time.time()
        with open(FILE_PATH, 'r') as f:
            cities = f.readlines()

            for city in cities:
                print('Getting Info on {}...'.format(city))
                response = self.api_request(url, city)
                _df = self.create_df(response)
                df = pd.concat([df, _df])

        print("Total Time : {} ".format(time.time()-start))
        self.save_df(df)
        print('Scrapping finieshed!')

        return df


if __name__ == "__main__":
    config = {}
    myScrapper = Scrapper()
    mydf = myScrapper.run()
