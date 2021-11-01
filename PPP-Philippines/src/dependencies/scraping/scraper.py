import requests
from bs4 import BeautifulSoup
import pandas as pd


class PhilippinesProjects:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config")

    def extract_links(self):
        """Adding self.config['count'] that tells extract_links function the
        number of links to extract. If not provided, it is set to None and
        all available links are extracted."""
        try:
            if self.config['count'] or self.config['count'] is None:
                pass
        except KeyError:
            self.config['count'] = None

        """Extracting links with relevant data"""
        root = 'https://ppp.gov.ph/project-database/'
        basepage = requests.get(root)
        soup = BeautifulSoup(basepage.text, 'html.parser')

        links = []
        for td in soup.find_all('td', class_='title'):
            for anchor in td.find_all('a'):
                links.append(anchor['href'])
            if self.config['count']:
                if len(links) == self.config['count']:
                    break
        return links

    def load_data(self, links):
        """Function to load data"""
        """Adding self.config['cols'], a Python list that tells load_data() to
        extract only the fields mentioned and not others. If not provided,
        it is set to None and all available fields are extracted."""
        try:
            if self.config['cols']:
                for col in self.config['cols']:
                    self.config['cols'].remove(col)
                    col = col.strip()
                    col = col.replace(' ', '_')
                    col = col.lower()
                    self.config['cols'].append(col)
            else:
                pass
        except KeyError:
            self.config['cols'] = None

        df = pd.DataFrame()
        for link in links:
            info_pg = requests.get(link)
            info_soup = BeautifulSoup(info_pg.text, 'html.parser')

            temp = {}
            name = info_soup.find('h2', class_='post-title').text.strip()
            temp['name_of_project'] = name
            for i in info_soup.find_all('h6'):
                fname = i.text.strip()
                if fname != '':
                    fname = fname.replace(' ', '_')
                    fname = fname.lower()
                    print(fname)
                    if self.config['cols']:
                        if fname in self.config['cols']:
                            for sib in i.next_siblings:
                                sibtext = sib.text.strip()
                                if sib.name == 'p':
                                    temp[str(fname)] = sibtext
                                elif sib.name == 'h6' and sibtext != '':
                                    break
                    else:
                        for sib in i.next_siblings:
                            if sib.name == 'p':
                                temp[str(fname)] = sib.text.strip()
                            elif sib.name == 'h6' and sib.text.strip() != '':
                                break
            df = df.append(temp, ignore_index=True)
        return df

    def run(self):
        """Load data, do_something and finally save the data"""
        links = self.extract_links()
        df = self.load_data(links)
        return df


if __name__ == "__main__":
    config = {'count': None, 'cols': None}
    obj = PhilippinesProjects(config=config)
    obj.run()
