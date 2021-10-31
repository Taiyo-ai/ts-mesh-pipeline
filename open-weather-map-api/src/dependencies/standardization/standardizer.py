import os
import pandas as pd

DATA_DIR = '../geocoding/geocoded_metadata.csv'

class Standardizer:

	def __init__(self,**kwargs):
	
		config = kwargs.get("config")
		self.sample_frequency = config['sample_frequency']
		self.name = config['name']
		self.description = config['description']
		self.units = config['units']
		self.url = config['url']
		
		
	def load_data(self):
		"""load csv file from the directory"""
		
		df_clean = pd.read_csv(DATA_DIR)
		
		return df_clean
	
	def create_metadata(self):
		"""creae the global fields standard"""
	
		columns = ['aug_id', 'original_id', 'sample_frequency', 'name','description',
			'units','source', 'url', 'domain', 'subdomain', 'country_name',
			'region_name', 'region_code', 'city', 'location', 'map_coordinates',
			'timestamps']  
		
		df = pd.DataFrame(columns=columns)
		
		return df
		

	def get_identifier(self,df,_df):
		"""get identifier fields values"""
		
		df['aug_id'] =  _df['id'].apply(lambda x : 'openweather_map_api_' + str(x))
		df['original_id'] = _df['id']
		df['sample_frequency'] = self.sample_frequency #fill(self.sample_frequency, inplace=True)
		
		return df
		
	def get_basic_specs(self,df):
		"""get basic specs fields values"""
		
		df['name'] = self.name
		df['description'] = self.description
		df['units'] = self.units
		
		return df
	
	def get_url(self,df):
		"""get url fields"""
		
		df['url'] = self.url
		
		return df
	
	def get_locations_info(self,df,_df):
		"""get locations fields"""
		
		#_df = pd.read_csv(DATA_DIR) #laod the geocoded daat
		df['country_name'] = _df['country_name']
		df['country_code'] = _df['country_code']
		df['region_name'] = _df['region_name']
		df['region_code'] = _df['region_code']
		df['city'] = _df['city']
		df['location'] = _df['location']
		df['map_coordinates'] = _df['map_coordinates']
		return df  
	
	def get_timestamps(self,df,_df):
		"""get timestamps"""
		
		#_df = pd.read_csv(DATA_DIR)
		df['timestamps'] = _df['timestamps']
		return df
		
	def save_data(self,df):
		"""save the data """
	
		df.to_csv('final_metadata.csv')
		return df
		
	def run(self):
		"""perform standarizer operations"""
		
		print('Performing Standardization operations...')
		_df = self.load_data()
		df = self.create_metadata()
		df = self.get_identifier(df,_df)
		df = self.get_basic_specs(df)
		df = self.get_url(df)
		df = self.get_locations_info(df,_df)
		df = self.get_timestamps(df,_df)
		df = self.save_data(df)
		print('Standardization finished!')
		
		return df
	
if __name__ == "__main__":
    config = {'sample_frequency' : 'daily', 
    	'name': 'open weather map api', 
    	'description' : 'weather forecast for next 30 days that inlcude wind speed, humidity, tempurature and pressure', 
    	'units' : 'celcius', 
    	'url' : 'https://community-open-weather-map.p.rapidapi.com/climate/month' }
    myStandardizer = Standardizer(config=config)
    mydf = myStandardizer.run()
    
