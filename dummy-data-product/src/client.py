from dependencies.scraping.scraper import Scraper
from dependencies.cleaning.cleaning import clean_data
from dependencies.geocoding.geocoder import geocode_data
from dependencies.standardization.standardizer import standardize_data
from dependencies.Vizualization.vizualization import viz_data
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_pipeline():
    # Initialize scraper
    location = input('Enter Location/Topic to search: ').lower()
    scraper = Scraper(location)
    
    # Scrape data
    
    scraped_data = scraper.scrape_data()
    #scraped_data.selenium_webdriver()
    
    # Clean data
    cleaned_data = clean_data(scraped_data)
    
    # Geocode data
    geocoded_data = geocode_data(cleaned_data)
    
    # Standardize data
    standardized_data = standardize_data(geocoded_data)
    
    # Generate output (e.g., save as CSV)
    # You can modify this section based on your specific requirements

    ## Some Visualisations on IEG Data: World Bank Project Ratings and Lessons
    viz_datas = viz_data()


    
if __name__ == '__main__':
    run_pipeline()
