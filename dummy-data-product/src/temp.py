import requests
from bs4 import BeautifulSoup
import json

url = "https://www.earthdata.nasa.gov/engage/open-data-services-and-software/api"

response = requests.get(url)

print(response.headers)
soup = BeautifulSoup(response.text, "html.parser")

data = soup.find_all('div')

n = 0
for i in data:
    print(n)
    n += 1
    d = i
    print(d)
