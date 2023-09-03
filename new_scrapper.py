import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://ieg.worldbankgroup.org/data'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    paragraphs = []
    for p in soup.find_all('p'):
        paragraphs.append(p.get_text())
    
    data = pd.DataFrame({'Text': paragraphs})
    
    data.to_csv('worldbank_data.csv', index=False)
    
    print('Scraping completed and data saved to worldbank_data.csv')
else:
    print('Failed to retrieve the web page. Status code:', response.status_code)
