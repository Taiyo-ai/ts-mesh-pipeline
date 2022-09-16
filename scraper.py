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

    '''Let's get the api link to scrap data from graph '''
    tender_info_link = []
    for link in countries_link[5:38]:
        href = link.get('href')
        tender_info_link.append(href[1:3])

    '''Let's make post request country by country to get json data '''   
    year = []
    print('Getting json data please wait ')
    for ch in tender_info_link:
        new  = requests.post(f'https://opentender.eu/api/{ch}/home/stats', json = {'lang': 'en'}).json()
        year.append(new['data']['histogram'])

    '''Page by Page Country and Total years in a formatted dictionary'''
    eu = {}
    print('Setting the data please wait...')
    for i in range(len(links)):
        res = requests.get(links[i])
        page = res.text
        read = BeautifulSoup(page, 'html.parser')
        country = read.find_all('span')
    
        eu[country[2].text] = year[i]
    
    print('Thank you! The Data is ready.')

    '''Data Prepration using pandas '''

    df1 = DataFrame(eu)
    data = df1.T
    data['Total Tenders'] = total_tenders
    

    '''CSV file conversion'''
    data.to_csv('scrapper.csv', encoding='utf-8', index= True)