import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd

class get_data:

  def __init__(self,soup):
    self.soup=soup

  def get_dataset(self):
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
    d={}
    job=self.soup.find('div',id="cmsContent").find('ul').find('a',href='/statistics/full_credit_gap_csv.zip')
    data=pd.read_csv('https://www.bis.org'+job['href'])
    for i in range(len(data)):
      country=data["Borrowers' country"][i][3:]
      if country not in d:
        d[country]=[data["Time Period"][i]]
      else:
        d[country].append(data["Time Period"][i])
    df=pd.DataFrame(d)
    df.to_csv('csv_files/Credit_to_gdp_gaps.csv',index=False)

html_text=requests.get('https://www.bis.org/statistics/full_data_sets.htm')
soup=BeautifulSoup(html_text.text,'lxml')
scrapper=get_data(soup)
scrapper.get_dataset()
scrapper.get_gdp_to_credit()
print('Done')