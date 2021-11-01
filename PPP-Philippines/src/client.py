from dependencies.scraping import scraper
from dependencies.cleaning import cleaning


# scraping the website
scraper_config = {'count': 5}
scraper_obj = scraper.PhilippinesProjects(config=scraper_config)
df = scraper_obj.run()
df.to_csv('../intermediate_files/scraped.csv')  # saving scraped data

# cleaning the data
cleaning_config = {'df': df}
cleaning_obj = cleaning.DataCleaner(config=cleaning_config)
df = cleaning_obj.run()
df.to_csv('../intermediate_files/cleaned.csv')
print(df['winning_bidder/s'])
