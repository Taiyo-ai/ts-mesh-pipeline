import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd


class requiresData:
    url = 'https://opentender.eu/all/download'
    r = requests.get(url)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent,'html.parser')
    value = soup.find_all(attrs={'class': 'container-outer downloads'})
    downloadRow = soup.find_all(attrs={'class': 'download-row'})
print(requiresData.downloadRow)
