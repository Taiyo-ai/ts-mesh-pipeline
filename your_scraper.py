import requests
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://www.nnvl.noaa.gov/view/globaldata.html'


response = requests.get(url)


if response.status_code == 200:
    
    soup = BeautifulSoup(response.text, 'html.parser')

    
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    
    
    data = pd.DataFrame({'https://ieg.worldbankgroup.org/data': links})
    
    
    data.to_csv('noaa_links.csv', index=False)
    
    print('Scraping completed and data saved to noaa_links.csv')
else:
    print('Failed to retrieve the web page. Status code:', response.status_code)
