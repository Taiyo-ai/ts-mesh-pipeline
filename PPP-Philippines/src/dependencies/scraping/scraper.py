from numpy.core.numeric import array_equal
import requests
from bs4 import BeautifulSoup
import pandas as pd

class MyClass:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config")

    def extract_links(self):
        """Adding self.config['count'] that tells extract_links function the
        number of links to extract. If not provided, it is set to None and
        all available links are extracted."""
        try:
            if self.config['count'] or self.config['count']==None:
                pass
        except:
            self.config['count'] = None
        
        """Extracting links with relevant data"""
        root = 'https://ppp.gov.ph/project-database/'
        basepage = requests.get(root)
        soup = BeautifulSoup(basepage.text, 'html.parser')

        links = []
        for td in soup.find_all('td', class_ = 'title'):
            for anchor in td.find_all('a'):
                links.append(anchor['href'])
            if self.config['count']:
                if len(links) == self.config['count']:
                    break
        return links

    def load_data(self, links):
        """Function to load data"""
        df = pd.DataFrame()
        for link in links:
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

    def save_data(self, df):
        """Function to save data"""
        df.to_csv('scraped_data.csv')

    def run(self):
        """Load data, do_something and finally save the data"""
        links = self.extract_links()
        df = self.load_data(links)
        self.save_data(df)


if __name__ == "__main__":
    config = {'count': None}
    obj = MyClass(config = config)
    obj.run()
