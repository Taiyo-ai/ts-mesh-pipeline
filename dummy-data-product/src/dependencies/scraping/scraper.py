# LIBRARIES TO BE INSTALLED

## !pip install requests
## !pip install prettytable
## !pip install matplotlib
## !pip install pandas

import requests
import json
import prettytable
import matplotlib.pyplot as plt
import pandas as pd

class BLS:
    def __init__(self,start_year,end_year,series_id):
        self.start_year = start_year
        self.end_year = end_year
        self.series_id = series_id
       
    def load_data(self):
        headers = {'Content-type': 'application/json'}
        data = json.dumps({"seriesid": [self.series_id],"startyear":self.start_year, "endyear":self.end_year})
        p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
        json_data = json.loads(p.text)
       
        return json_data
   
    def save_data(self):
        for series in self.load_data()['Results']['series']:
            x=prettytable.PrettyTable(["series id","year","period","value","footnotes"])
            seriesId = series['seriesID']
            for item in series['data']:
                year = item['year']
                period = item['period']
                value = item['value']
                footnotes=""
                for footnote in item['footnotes']:
                    if footnote:
                        footnotes = footnotes + footnote['text'] + ','
                if 'M01' <= period <= 'M12':
                    x.add_row([seriesId,year,period,value,footnotes[0:-1]])

            output = open(seriesId + '.csv','w')

            output.write (x.get_string())
            output.close()
        return x
   
    def presentation_of_data(self):
        id=''
        for i in self.load_data()['Results']['series']:
            id=i['seriesID']
            bls_data=pd.DataFrame(i['data'])
            bls_data.insert(0,'ID',id)
           
        plt.bar(bls_data['year'],bls_data['value'])
        plt.yscale('linear')
        plt.xlabel('Years',fontsize=15)
        plt.ylabel(bls_data['ID'][0],fontsize=15)
        plt.title('Representaion of Data',fontsize=20)
        plt.show()
       
    def run(self):
        self.load_data()
        self.save_data()
        self.presentation_of_data()
        return


## series_id to extract different data
series_id={'Unemployment Rate':'LNS14000000','Civilian Employment':'LNS12000000','Civil Labour Force':'LNS11000000'}

## Unemployment Rate Data
data=BLS('2016','2022',series_id['Unemployment Rate'])
data.run()

## Civilian Employment Data
data=BLS('2016','2022',series_id['Civilian Employment'])
data.run()

## Civil Labour Force Rate
data=BLS('2016','2022',series_id['Civil Labour Force'])
data.run()
