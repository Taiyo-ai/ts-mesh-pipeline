# import your dependencies here
from cleaning import cleaner
from scraping import scraper
from standardization import standardizer
 
 
class MyClass:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config")

    def do_something(self):
        """Do extraction or processing of data here"""
        extracted_data = scraper.dataScrapper()
        return extracted_data

    def load_data(self):
        """Function to load data"""
        # load data from source in the form of dataframe
        cleaned_data = cleaner.dataCleaner()
        cleaned_data = cleaned_data.head()
        return cleaned_data

    def save_data(self):
        """Function to save data"""
        data = standardizer.dataStandardizer()
        return data

    def run(self):
        """Load data, do_something and finally save the data"""
        #scrapped data
        print("\nScrapping data.....")
        scraper.dataScrapper()
        print("\nData scrapped successfully!!!")
        
        # Transformed data
        print("\nTransforming data please! wait for a moment....")
        cleaner.dataCleaner()
        print("\nData transformed successfully!!!")
        
        # Load data ...
        print("\nLoading data please! wait for a moment....")
        standardizer.dataStandardizer()
        print("\nData loaded successfully!!!")
        


if __name__ == "__main__":
    config = {}
    obj = MyClass(config = config)
    obj.run()
