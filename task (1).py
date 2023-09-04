import requests
from bs4 import BeautifulSoup
import csv

class WebScraper:
    def __init__(self, url):
        self.url = url

    def scrape_data(self):
        try:
            # Send an HTTP GET request to the URL
            response = requests.get(self.url)

            # Check if the request was successful
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Implement scraping logic here
                # Example: Extract data from the website
                data = []

                # Replace this logic with the actual scraping logic
                # Example:
                for item in soup.find_all('div', class_='item'):
                    title = item.find('h2').text
                    description = item.find('p').text
                    data.append([title, description])

                return data
            else:
                print(f"Failed to retrieve data. Status code: {response.status_code}")
                return None

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def save_to_csv(self, data, filename):
        try:
            with open(filename, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                # Write header if needed
                # csv_writer.writerow(['Title', 'Description'])
                csv_writer.writerows(data)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error while saving data to CSV: {str(e)}")

if __name__ == "__main__":
    # Replace 'https://example.com' with the URL of the website you want to scrape
    url_to_scrape = 'https://www.earthdata.nasa.gov/engage/open-data-services-and-software/api'
    
    # Initialize the scraper
    scraper = WebScraper(url_to_scrape)
    
    # Scrape data
    scraped_data = scraper.scrape_data()
    
    if scraped_data:
        # Specify the filename where you want to save the data
        csv_filename = 'scraped_data.csv'
        
        # Save the data as a CSV file
        scraper.save_to_csv(scraped_data, csv_filename)
