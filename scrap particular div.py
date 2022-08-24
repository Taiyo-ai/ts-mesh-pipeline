# This will scrape particular div id from webpage
from bs4 import BeautifulSoup
import requests

url = "https://www.bls.gov/news.release/laus.nr0.htm"

html_content = requests.get(url).text
soup = BeautifulSoup(html_content, "html.parser")

texts = soup.find_all('pre')
for text in texts:
    print(text.get_text())
