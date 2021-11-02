from dependencies.scraping import scraper
from dependencies.cleaning import cleaning
from dependencies.geocoding import geocoder
from dependencies.standardization import standardizer


#my config 
standardizer_config = {'sample_frequency' : 'daily', 
    	'name': 'open weather map api', 
    	'description' : 'weather forecast for next 30 days that inlcude wind speed, humidity, tempurature and pressure', 
    	'units' : 'celcius', 
    	'url' : 'https://community-open-weather-map.p.rapidapi.com/climate/month' }


#construt the object class
myScrapper = scraper.Scrapper()
myCleaner = cleaning.Cleaner()
myGeocoder = geocoder.Geocoder()
myStandardizer = standardizer.Standardizer(config=standardizer_config)

#run all the steps to generate the necessery data and perform operatios
#myScrapper.run()
myCleaner.run()
myGeocoder.run()
myStandardizer.run()
