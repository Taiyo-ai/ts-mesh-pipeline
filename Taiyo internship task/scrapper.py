import csv
from csv import writer
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

class get_data:

  def __init__(self,soup):
    self.soup=soup

  def get_dataset(self):                                                              # get list of datasets and links
    data=[]
    job=self.soup.find('div',id="cmsContent").find('ul').find_all('li')
    for i in job:
      a=i.find('a')
      link="https://www.bis.org"+a['href']
      data.append({'dataset_name':a.text,'link':link})
    with open('csv_files/dataset_list.csv','w') as f:
      w=csv.DictWriter(f,['dataset_name','link'])
      w.writeheader()
      w.writerows(data)

  def get_gdp_to_credit(self):                                                       
    d = {}
    job = soup.find('div', id="cmsContent").find('ul').find('a', href='/statistics/full_credit_gap_csv.zip')
    data = pd.read_csv('https://www.bis.org' + job['href'])
    ref = [np.insert(data['Frequency'].unique(), 0, 'Frequency'),
           np.insert(data["Borrowers' country"].unique(), 0, 'Country'),
           np.insert(data['Borrowing sector'].unique(), 0, 'Borrowing Sector'),
           np.insert(data['Lending sector'].unique(), 0, 'Lending Sector'),
           np.insert(data['Credit gap data type'].unique(), 0, 'Credit gap data type')]
    d['Time Period'] = data["Time Period"]

    for i in range(len(data)):
      country = data["Borrowers' country"][i][3:]
      if country not in d:
        d[country] = ""
    df = pd.DataFrame(d)

    with open('csv_files/final_output.csv', 'w') as f:
      w = writer(f)
      w.writerows(ref)

    df.to_csv('csv_files/final_output.csv', mode='a', index=False)

html_text=requests.get('https://www.bis.org/statistics/full_data_sets.htm')
soup=BeautifulSoup(html_text.text,'lxml')
scrapper=get_data(soup)
scrapper.get_dataset()
scrapper.get_gdp_to_credit()
print('Done')
