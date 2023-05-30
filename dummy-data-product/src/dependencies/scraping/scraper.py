import requests
import json
import os
import pandas as pd
import time
from selenium import webdriver
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self,location):
        # Initialize your scraper here
        self.location = location
    

    def scrape_data(self):
        # Start the Driver
        driver = webdriver.Chrome(executable_path=r"C:\Users\prngr\Downloads\chromedriver.exe")
        
        # Hit the url of NASA Earth Data website and wait for 15 seconds.
        url = 'https://earthdata.nasa.gov/search?keys={location}'.format(location=self.location)
        driver.get(url)
        time.sleep(2)
        
        # Fetch the webpage and store in a variable.
        webpage = driver.page_source
        
        # Parse the page using BeautifulSoup
        HTMLPage = BeautifulSoup(webpage, 'html.parser')
        
        datas = []
        results = HTMLPage.find_all(class_='views-row')
        #print(results)
        for lists in results:
            title = lists.find(class_="search-title").text.strip()
            description = lists.find('span',class_="field-content").text.strip()
            link = 'https://www.earthdata.nasa.gov/' + lists.find('a')['href']
            datas.append({'Title':title,'Description':description ,'Link': link})
        
        #Create a DataFrame
        df = pd.DataFrame(datas)
        
        #display(df)
        filename = 'Scraping_output_'+self.location+'.csv'
        # Store to csv file
        # df.to_excel(filename, sheet_name=self.location, index=False, header=True)
        df.to_csv(filename, sep=',', index=False, header=True)
        
        #For Page UP
        page=999
        
        for i in range(1,page):
            url = 'https://earthdata.nasa.gov/search?keys={}&page={}'.format(self.location, i)
            driver.get(url)
            time.sleep(2)
            # Fetch the webpage and store in a variable.
            webpage = driver.page_source
            # Parse the page using BeautifulSoup
            HTMLPage = BeautifulSoup(webpage, 'html.parser')
            datas = []
            results = HTMLPage.find_all(class_='views-row')
            #print(results)
            if len(results) == 0:
                break
            else:
                for lists in results:
                    title = lists.find(class_="search-title").text.strip()
                    description = lists.find('span',class_="field-content").text.strip()
                    link = 'https://www.earthdata.nasa.gov/' + lists.find('a')['href']
                    datas.append({'Title':title,'Description':description ,'Link': link})
        
                #Create a DataFrame
                df = pd.DataFrame(datas)
        
                #display(df)
                
                # Store to csv file
                df.to_csv(filename,mode='a',index=False,header=False)
                # with pd.ExcelWriter(filename, engine='openpyxl', mode='a') as writer:
                #     writer.book = writer.book
                #     df.to_excel(writer,sheet_name=self.location,index=False, header=False)
            
        
        print('Web Scraping Successful!')
        print('Please check the file named as'+filename+' in the folder')
        return filename
