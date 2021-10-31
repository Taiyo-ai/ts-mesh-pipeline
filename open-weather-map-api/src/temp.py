import requests
from datetime import datetime
import pandas as pd
from pandas import json_normalize 

"""
fields = {'dt', 'humidity','pressure', 'temp': {'', 'average_max', 'average_min', 'record_max' ,'record_min'}, 'wind_speed'}
columns = ['id', 'city', 'country', 'date', 'humidity', 'pressure', 'average_temp','average_max_temp', 'average_min_temp', 'record_max_temp', 'record_min_temp','wind_speed'
			]

columns = ['id','city','country','date','values']


### API request
url = "https://community-open-weather-map.p.rapidapi.com/climate/month"

querystring = {"q":"New York"}

headers = {
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
    'x-rapidapi-key': "0853b11a2dmsh562d6f9daefc256p1cfc7fjsn7a0dfc4cf285"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
###
d = []

uid =response.json()['city']['id']
city = response.json()['city']['name']
country = response.json()['city']['country']
df2 = pd.DataFrame({'id': [uid for _ in range(30)], 'city': [city for _ in range(30)], 'country': [country for _ in range(30)]})

df1 = json_normalize(response.json()['list'])

#df['city'].fillna(country,inplace=True) #clreaning part




for i in range(30):
	
	#dt =int(response.json()['list'][i]['dt'])
	d.append([response.json()['city']['id'],
		response.json()['city']['name'],
		response.json()['city']['country'],
		datetime.utcfromtimestamp(int(response.json()['list'][i]['dt'])).strftime('%Y-%m-%d'),
		response.json()['list'][i]['humidity']
		])
	
	
	[uid =response.json()['city']['id'],
		city = response.json()['city']['name'],
		country = response.json()['city']['country'],
		date = datetime.utcfromtimestamp(int(response.json()['list'][i]['dt'])).strftime('%Y-%m-%d')
		values = response.json()['list'][i]['wind_speed']
		])
	
	#print(datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S'))


#create a data frame


	
df = pd.DataFrame(data=d,columns=columns)
print(df)

"""


#check for geocoding 


import requests
import urllib.parse

city = "Tokyo"
country = ""
url = "https://nominatim.openstreetmap.org/?addressdetails=1&q=" + city + "+" + country +"&format=json&limit=1"

response = requests.get(url).json()
print(response)
print(response[0]["lat"])
print(response[0]["lon"])





