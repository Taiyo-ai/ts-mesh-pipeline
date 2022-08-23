import datacommons 
import datacommons_pandas
from geopy import Nominatim
import pandas as pd
from bs4 import BeautifulSoup
import requests


class DCHarvester:

    def __init__(self,country_name,stat_var):
        geo = Nominatim(user_agent='taiyo_app')
        self.country_name = country_name
        self.stat_var = stat_var
        self.loc = geo.geocode(country_name)
        self.lat,self.long = self.loc.latitude,self.loc.longitude


    def __get_raw_series(self,):
        self.series = datacommons_pandas.build_time_series('country/'+self.country_name,stat_var=self.stat_var)
        return self.series


    def __add_standards(self):
        self.df = pd.DataFrame(self.__get_raw_series()).reset_index()
        self.df['aug_id'] = ['DC'+j['index'] for i,j in self.df.iterrows()]
        self.df['Domain'] = ['Data Commons' for i in range(len(self.df))]
        self.df['Coordinates'] = [[self.lat,self.long] for i in range(len(self.df))]


        return self.df

    def get_series(self):
        return self.__add_standards()







