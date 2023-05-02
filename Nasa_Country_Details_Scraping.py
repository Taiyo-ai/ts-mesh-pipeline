from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

class Web_Scraping:
    
    def __init__(self, query, num_pages):
        self.query = query
        self.num_pages = num_pages
      
    def extract_data(self):
        driver = webdriver.Chrome(executable_path = r"C:\Users\Aditya\Downloads\chromedriver_win32\chromedriver.exe")
        
        home_url = f'https://www.earthdata.nasa.gov/search?keys={self.query}'
        driver.get(home_url)
        time.sleep(2)
        
        for i in range(0,2):
            driver.execute_script("window.scrollBy(0,6000)")
            time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        results = soup.find('div', attrs={'class': 'view-content row'})

        titles = []
        description = []
        links = []

        for lists in results.find_all('div', attrs={'class': 'mb-3 views-row'}):
            title_elems = lists.find_all('div', attrs={'class': 'search-title'})
            if len(title_elems) > 1:
                for title_elem in title_elems:
                    if title_elem.find('a'):
                        break
                else:
                    title_elem = title_elems[0]
            else:
                title_elem = title_elems[0]

            des_elem = lists.find('div', attrs={'class':'views-field views-field-field-summary search-description'})
            if des_elem and des_elem.text:
                des = des_elem.text.strip()
            else:
                des_elem = lists.find('div', attrs={'class':'views-field views-field-field-short-description'})
                if des_elem and des_elem.text:
                    des = des_elem.text.strip()
                else:
                    des_elem = lists.find('div', attrs={'class':'views-field views-field-description search-description'})
                    if des_elem and des_elem.text:
                        des = des_elem.text.strip()
                    else:
                        des = ''

            link_elem = lists.find('div', attrs={'class':'views-field views-field-url'})

            if title_elem and title_elem.text:
                title = title_elem.text.strip()
                titles.append(title)
            else:
                title = ''

            if link_elem and link_elem.text:
                link = link_elem.text.strip()
                links.append(link)
            else:
                link = ''

            description.append(des)

        home_df = pd.DataFrame(list(zip(titles, description, links)),
               columns =['title', 'description', 'link'])
        
        for page_num in range(2, self.num_pages+1):
            # Send a GET request to each additional page
            url = f'https://www.earthdata.nasa.gov/search?keys={self.query}&page={page_num}'
            driver.get(url)
            time.sleep(2)
            
            for i in range(0,2):
                driver.execute_script("window.scrollBy(0,6000)")
                time.sleep(2)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

        results = soup.find('div', attrs={'class': 'view-content row'})

        titles = []
        description = []
        links = []

        for lists in results.find_all('div', attrs={'class': 'mb-3 views-row'}):
            title_elems = lists.find_all('div', attrs={'class': 'search-title'})
            if len(title_elems) > 1:
                for title_elem in title_elems:
                    if title_elem.find('a'):
                        break
                else:
                    title_elem = title_elems[0]
            else:
                title_elem = title_elems[0]

            des_elem = lists.find('div', attrs={'class':'views-field views-field-field-summary search-description'})
            if des_elem and des_elem.text:
                des = des_elem.text.strip()
            else:
                des_elem = lists.find('div', attrs={'class':'views-field views-field-field-short-description'})
                if des_elem and des_elem.text:
                    des = des_elem.text.strip()
                else:
                    des_elem = lists.find('div', attrs={'class':'views-field views-field-description search-description'})
                    if des_elem and des_elem.text:
                        des = des_elem.text.strip()
                    else:
                        des = ''

            link_elem = lists.find('div', attrs={'class':'views-field views-field-url'})

            if title_elem and title_elem.text:
                title = title_elem.text.strip()
                titles.append(title)
            else:
                title = ''

            if link_elem and link_elem.text:
                link = link_elem.text.strip()
                links.append(link)
            else:
                link = ''

            description.append(des)
        df = pd.DataFrame(list(zip(titles, description, links)),
               columns =['title', 'description', 'link'])
        
        merged_df = pd.concat([home_df, df], axis=0)


        merged_df.to_csv('Nasa_Country_Details.csv', sep=',', index=False)
        print('Web Scraping Successful!')
query = input('Enter Location: ').lower()
num_pages = int(input('Enter number of pages to scrape: '))
ws = Web_Scraping(query, num_pages)
ws.extract_data()