import os
import pandas

class Cleaner:
	def __init__(self):
		return None
	
	def remove_duplcates(self,df):
		"""remove duplicates row in the datframe"""
				
		df.drop_duplictaes(keep='first', inplace=True)
		return df
		
	
	def check_missing_values(self,df):
		"""check for missing values replace it with NaN"""
		df.replace(' ', NaN)
		return df
	
	

			
	def country_iso_code(self,df):
	"""convert country codes to ISO 3166-1 alpha3"""
	
		return df
	
	def convert_to_datetime(self,df):
		""" """
		dt =df['date']
		date = datetime.utcfromtimestamp().strftime('%Y-%m-%d')
		return df

if __name__ == "__main__":
    config = {}
    myScrapper = Scrapper()
    mydf = myScrapper.run()
    
		
