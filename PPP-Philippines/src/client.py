from dependencies.scraping import scraper
from dependencies.cleaning import cleaning
from dependencies.geocoding import geocoder


# scraping the website
print("Scraping the website...")
scraper_config = {'count': 5}
scraper_obj = scraper.PhilippinesProjects(config=scraper_config)
df = scraper_obj.run()
df.to_csv('../intermediate_files/scraped.csv')  # saving scraped data

# cleaning the data
print('Cleaning data...')
cleaning_config = {'df': df}
cleaning_obj = cleaning.DataCleaner(config=cleaning_config)
df = cleaning_obj.run()
df.to_csv('../intermediate_files/cleaned.csv')

# geocoding regions
print('Geocoding locations...')
geocoding_config = {'df': df}
geocoding_obj = geocoder.GeocodingRegion(config=geocoding_config)
df = geocoding_obj.run()
df.to_csv('../intermediate_files/geocoded.csv')
