import requests
import pandas as pd
from bs4 import BeautifulSoup

class NASAEarthDataScraper:
    def __init__(self):
        self.base_url = "https://www.earthdata.nasa.gov/engage/open-data-services-and-software/api"
        self.data = []

    def scrape(self):
        # Send an HTTP GET request to the URL
        response = requests.get(self.base_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the elements containing data (you'll need to inspect the website's structure)
            # For this example, let's say we're looking for links to datasets
            dataset_links = soup.find_all('a', class_='dataset-link')

            # Extract data from the elements
            for link in dataset_links:
                dataset_name = link.text
                dataset_url = link['href']
                self.data.append({'Dataset Name': dataset_name, 'Dataset URL': dataset_url})

            print("Scraping completed.")
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)

    def save_to_csv(self, filename):
        if self.data:
            df = pd.DataFrame(self.data)
            df.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
        else:
            print("No data to save.")

# Example usage:
if __name__ == "__main__":
    scraper = NASAEarthDataScraper()
    scraper.scrape()
    scraper.save_to_csv("nasa_earth_data.csv")
