from dependencies.scraping import scraper


config = {'count': None}
obj = scraper.MyClass(config=config)
df = obj.run()
