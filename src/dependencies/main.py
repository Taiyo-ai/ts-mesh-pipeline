from scraper.scrape import Scraper
from cleaner.cleaner import Cleaner
from geocoding.geocoding import CSVConverter

if __name__ == '__main__':
    scraper_object = Scraper()
    cleaner_object = Cleaner()
    # scraper_object.scrape_data()
    cleaner_object.cleaner()
    '''Give the DF and Column Name to get Geocoding'''
    geocode_object = CSVConverter(r'C:\Users\ox\PycharmProjects\Prism_v01\Taiyo\Sats_Kanna\cleaner.csv', 'Region')
    geocode_object.get_coordinates()