import os
import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_nasa(query: str, num_pages: int) -> pd.DataFrame:
    base_url = 'https://www.earthdata.nasa.gov'
    search_url = f'{base_url}/search?keys={query}'

    def scrape_page(page_url):
        try:
            response = requests.get(page_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find('div', attrs={'class': 'view-content row'})
            data = []
            for lists in results.find_all('div', attrs={'class': 'mb-3 views-row'}):
                title_elem = lists.find('div', attrs={'class': 'search-title'}).find('a')
                title = title_elem.text.strip() if title_elem else ''
                des_elem = lists.find('div', attrs={'class': 'views-field views-field-field-summary search-description'})
                des = des_elem.text.strip() if des_elem else ''
                link_elem = lists.find('div', attrs={'class': 'views-field views-field-url'})
                link = f"{base_url}{link_elem.find('a')['href']}" if link_elem else ''
                data.append((title, des, link))
            return pd.DataFrame(data, columns=['title', 'description', 'link'])
        except requests.exceptions.RequestException as e:
            logging.error(f'Error scraping page {page_url}: {e}')
            return pd.DataFrame()

    pages = range(1, num_pages+1)
    data = pd.concat([scrape_page(f'{search_url}&page={page_num}') for page_num in pages])
    if data.empty:
        logging.warning('No data was scraped.')
    return data


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    query = os.getenv('QUERY', 'india')
    num_pages = int(os.getenv('NUM_PAGES', 2))
    data = scrape_nasa(query, num_pages)
    if not data.empty:
        output_path = os.getenv('OUTPUT_PATH', 'Nasa_Country_Details1.csv')
        data.to_csv(output_path, sep=',', index=False)
        logging.info(f'Successfully scraped {len(data)} rows and saved to {output_path}.')
