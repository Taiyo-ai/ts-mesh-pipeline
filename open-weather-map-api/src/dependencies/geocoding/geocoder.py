import os
import pandas as pd
from geopy.geocoders import Nominatim
import geocoder as gc
import pycountry

DATA_DIR='../cleaning/cleaned_data.csv'

class Geocoder:

	def __init__(self):
		self.geolocator = Nominatim(user_agent="my_user_agent")
		#self.geolocator.geocode(x).longitude
	def load_data(self):
		"""load csv data from the directory"""
	
		df = pd.read_csv(DATA_DIR)
		return df
		
	def create_geocoded_metadata(self):
		"""create a dataframe for the metadata"""
		
		df_meta = pd.DataFrame()
		return df_meta
		
	def city_dict(self,df):
		"""initilaize a dict to store the city geo info"""
		cities = df['city'].unique()
		locations = {}
		for city in cities:
			if city not in locations.keys():
				locations[city] = {'address' : self.geolocator.geocode(city, language='en').address, 
				'coordinates' : [[self.geolocator.geocode(city, language='en').latitude,self.geolocator.geocode(city, language='en').longitude]]}
		
		return locations
		
		
	def get_locations_metadata(self,df,df_meta):
		"""get location based metadat"""
		
		df_meta['id'] = df['id']
		df_meta['country_name'] = df['country'].apply(lambda x : pycountry.countries.get(alpha_3=x).name)
		df_meta['country_code'] = df['country']
		df_meta['region_name'] = df['region_name']
		df_meta['region_code'] = df['region_code']
		df_meta['city'] = df['city']

		locations = self.city_dict(df)
		df_meta['location'] = df['city'].apply(lambda x : locations[x]['address'])
		df_meta['map_coordinates'] = df['city'].apply(lambda x : locations[x]['coordinates'])

		df_meta['timestamps'] = df['dt']
		return df_meta
		
	def save_data(self,df_meta):
		"""save data"""
		df_meta.to_csv('geocoded_metadata.csv')
		return df_meta
	
	def run(self):
		"""perform gecoder operations"""
		
		print('Performing Geocoding operations...')
		df = self.load_data()
		df_meta = self.create_geocoded_metadata()
		df_meta = self.get_locations_metadata(df,df_meta)

		df_meta = self.save_data(df_meta)
		print('Geocoding finished!')
		
		return df_meta
	

if __name__ == "__main__":
    config = {}
    myGeocoder = Geocoder()
    mydf = myGeocoder.run()
    
		
