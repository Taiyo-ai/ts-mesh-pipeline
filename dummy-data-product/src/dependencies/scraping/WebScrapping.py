
from bs4 import BeautifulSoup
import requests,openpyxl


class Scraping:
    def __init__(self,url):
        try:
            #creating a new work book
            excel = openpyxl.Workbook()
            sheet = excel.active
            #naming the excel sheet 
            sheet.title = 'webScrap'
            sheet.append(['Event Id','Event Name','End Date','End Time'])
            source = requests.get(url)
            source.raise_for_status()
            soup = BeautifulSoup(source.text,'html.parser')
            contracts = soup.find('tbody').find_all('tr')
            #looping through table rows
            for contract in contracts:
                tdlist = contract.find_all('td')
                datetime = tdlist[2].text.split('-')
                sheet.append([tdlist[0].a.text,tdlist[1].text,datetime[0],datetime[1]])
        
        except Exception as e:
            print(e)

        excel.save('webscraping.csv')


webScrap = Scraping('https://dot.ca.gov/programs/procurement-and-contracts/contracts-out-for-bid')
