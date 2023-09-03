import requests
from bs4 import BeautifulSoup

req=requests.get("https://ieg.worldbankgroup.org/data/")
soup=BeautifulSoup(req.content,"html.parser")
res=soup.title
print(res.prettify())
