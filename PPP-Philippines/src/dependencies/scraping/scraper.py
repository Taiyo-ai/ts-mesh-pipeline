import requests
from bs4 import BeautifulSoup
import pandas as pd

def main():
    root = 'https://ppp.gov.ph/project-database/'

    basepage = requests.get(root)
    soup = BeautifulSoup(basepage.text, 'html.parser')

    links = []
    for td in soup.find_all('td', class_ = 'title'):
        for anchor in td.find_all('a'):
            links.append(anchor['href'])

    df = pd.DataFrame()
    x = 0
    for link in links:
        x += 1
        if x ==5:
            break
        info_pg = requests.get(link)
        info_soup = BeautifulSoup(info_pg.text, 'html.parser')

        temp = {}
        temp['Name of Project'] = info_soup.find('h2', class_ = 'post-title').text.strip()
        for i in info_soup.find_all('h6'):
            for sib in i.next_siblings:
                if sib.name == 'p':
                    temp[str(i.text.strip())] = sib.text.strip()
                elif sib.name == 'h6':
                    break
        df = df.append(temp, ignore_index=True)
    return df

if __name__=='__main__':
    main()