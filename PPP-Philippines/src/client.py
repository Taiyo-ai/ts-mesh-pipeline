from dependencies.scraping import scraper
from dependencies.cleaning import cleaning


# scraping the website
scraper_config = {'count': 5}
scraper_obj = scraper.MyClass(config=scraper_config)
df = scraper_obj.run()
for col in df.columns:
    print(col)

# cleaning the data
cleaning_config = {'df': df}
cleaning_obj = cleaning.MyClass(config=cleaning_config)
cleaning_obj.run()
