import requests
import json
import os
import pandas as pd
import time
from selenium import webdriver
from bs4 import BeautifulSoup


class Web_Scraping:
    

        
    def selenium_webdriver(self):
        
        # Start the Driver
        driver = webdriver.Chrome(executable_path = r"C:\Users\laptop\Downloads\chromedriver_win32 (2).zip\chromedriver.exe")
        
        # Hit the url of NASA Earth Data website and wait for 15 seconds.
        url = 'https://www.earthdata.nasa.gov/engage/open-data-services-and-software/api'

        driver.get(url)
        time.sleep(15)
        
        # Driver scrolls down 25 times to load the table.
        for i in range(0,30):
            driver.execute_script("window.scrollBy(0,6000)")
            time.sleep(10)
            
        # Fetch the webpage and store in a variable.
        webpage = driver.page_source
        
        # Parse the page using BeautifulSoup
        HTMLPage = BeautifulSoup(webpage, 'html.parser')
        
        titles = []
        description = []
        links = []

        for lists in HTMLPage.find_all(class_ = 'result'):
            if (lists.span.text != '' and len(lists.find_all('p')) != 0):
                titles.append(lists.span.text)
                description.append(lists.find('p', class_ = '').text)
                links.append(lists.find('p', class_ = 'search-link').text)
        
        # Create a DataFrame
        df = pd.DataFrame(list(zip(titles, description, links)),
               columns =['title', 'description', 'link'])
        
        display(df)
        
        # Store to csv file
        df.to_csv('spdata.csv', sep=',', index=False,header=True)
        print ('suss')