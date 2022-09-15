#! python3
# scraper.py - Launches a website and scrapes the data into csv file

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from pandas import DataFrame, Series


class Scrapper:
    url = 'https://opentender.eu/'
    response = requests.get(url)

    try:
        response.raise_for_status()
    except Exception as exc:
        print('There was a problem.')

    page_contents = response.text
    soup = BeautifulSoup(page_contents, 'html.parser')

    '''All Availaible Countries Link in a list named links '''

    countries_link = soup.find_all('a',href = True)

    links = []
    for link in countries_link[5:38]:
        complete_link = 'https://opentender.eu' + link.get('href')
        links.append(complete_link)
    
    '''Total Tenders by each country'''

    no_of_tenders = soup.find_all('div')[21:54]
    tenders = []

    for num in no_of_tenders:
        tenders.append(num.text)

    '''Some Tenders are not in convert them into float'''

    reg = re.compile(r'\d+.?\d+')
    total_tenders = []

    for tend in tenders:
        if 'Million' in tend:
            mo = reg.findall(tend)
            corrected_num = float(mo[0]) * 1000000
            total_tenders.append(corrected_num)
        else:
            total_tenders.append(tend)

    '''Page by Page Country and Total years in a formatted dictionary'''
    year = {}
    eu = {}
    print('Script is running please wait...')
    for i in range(len(links)):
        res = requests.get(links[i])
        page = res.text
        read = BeautifulSoup(page, 'html.parser')
        country = read.find_all('span')
    
        years = read.find(class_ = 'x axis')
        num = years.find_all('title') 
    
        for sp in num:
            year[sp.text] = 0
        
        
        eu[country[2].text] = year
    
    print('Thank you! Results are here!!')

    '''Data Prepration using pandas '''

    df1 = DataFrame(eu)
    data = df1.T
    data['Total Tenders'] = total_tenders
    

    '''CSV file conversion'''
    data.to_csv('scrapper.csv', encoding='utf-8', index= True)