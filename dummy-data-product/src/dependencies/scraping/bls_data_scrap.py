import requests
from bs4 import BeautifulSoup
import pandas as pd


class bls_data:
    def __init__(self, series_id, survey):

        data = {
            "series_id": series_id,
            "survey": survey
        }
        self.get_data(data)

    def get_data(self, data):
        r = requests.post('https://data.bls.gov/cgi-bin/surveymost', data=data)
        soup = BeautifulSoup(r.text, 'lxml')
        s = soup.find('table', id='table0')

        headers = []
        for i in s.find_all('thead'):
            title = i.text
            headers.append(title)

        mydata = pd.DataFrame(columns=headers)

        for j in s.find_all('tbody')[1:]:
            for i in j.find_all('tr')[1:]:
                row_data = i.find_all('td')
                row = [i.text for i in row_data]
                length = len(mydata)
                mydata.loc[length] = row

        # Save Dataframe to CSV file
        mydata.to_csv('inflation_by_CPI.csv')


bls_data(['CUSR0000SA0', 'CUSR0000SETB01', 'CUSR0000SAF1', 'CUSR0000SETA02'], ['bls'])

