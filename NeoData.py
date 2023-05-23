import csv
import requests
from dotenv import load_dotenv
import os

class NEODataScraper:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file

    def scrape_data(self):
        start_date = '2023-01-01'  # Replace with your desired start date
        end_date = '2023-01-07'  # Replace with your desired end date
        # Replace with your NASA API key
        # Date range should be in one week range or api won't work
        api_key = os.getenv('API_KEY')

        url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print('Error: Failed to fetch data from the API.')
            print(response.content)
            return None

    def save_to_csv(self, data, filename):
        if data:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Date', 'NEO Name', 'Diameter (km)',
                                 'Close Approach Date', 'Miss Distance (km)'])

                for date in data['near_earth_objects']:
                    neo_list = data['near_earth_objects'][date]
                    for neo in neo_list:
                        row = [
                            date,
                            neo['name'],
                            neo['estimated_diameter']['kilometers']['estimated_diameter_max'],
                            neo['close_approach_data'][0]['close_approach_date_full'],
                            neo['close_approach_data'][0]['miss_distance']['kilometers']
                        ]
                        writer.writerow(row)

            print(f"Data saved to {filename} successfully.")
        else:
            print("No data to save.")


# Usage
scraper = NEODataScraper()
data = scraper.scrape_data()
if data:
    scraper.save_to_csv(data, 'neo_data.csv')
