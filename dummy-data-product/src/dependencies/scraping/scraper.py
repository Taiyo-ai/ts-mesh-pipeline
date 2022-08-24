import requests
from bs4 import BeautifulSoup
import pandas as pd

class Scrapper:
    r = requests.get('https://opentender.eu/start')
    html = r.text
    data = BeautifulSoup(html, 'html.parser')
    country=  []
    tenders = []
    for i in range(len(all_tender_link)):
        country.append(all_tender_link[i].a.text)
        tenders.append(all_tender_link[i].div.text)
        
    base_url = 'https://opentender.eu'
    link = []
    for i in range(len(all_tender_link)):
        t = all_tender_link[i].a['href']
        link.append(base_url + t.split('?')[0])
        
    dictionary = {}
    for i in range(0,len(link)):
        rs = requests.get(link[i])
        html_2 = rs.text
        tender_data = BeautifulSoup(html_2, 'html.parser')

        Year = []
        No_oF_Tender = []

        x = tender_data.find_all(class_ = 'x axis')[0]
        x = x.find_all('title')
        for j in range(len(x)):
            Year.append(int(x[j].text))

        y = tender_data.find_all(class_ = 'y axis')[0]
        y = y.find_all('title')
        for k in range(len(y)):
            No_oF_Tender.append(int(y[k].text))

        dictionary[country[i]] =  {'tenders': tenders[i], 'Year':Year, 'No_oF_Tender':No_oF_Tender}
    pd = pd.DataFrame.from_dict(dictionary)
    
Sc = Scrapper()
Sc.pd.to_csv('Scrapper.csv')
# print(Sc.dictionary)
