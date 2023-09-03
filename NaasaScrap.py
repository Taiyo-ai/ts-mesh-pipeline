import requests
import csv
import matplotlib.pyplot as plt

class NasaEarthDataScraper:
    def __init__(self, api_url, output_csv, output_image=None):
        self.api_url = api_url
        self.output_csv = output_csv
        self.output_image = output_image

    def scrape_data(self):
        try:
            # Send a GET request to the NASA Earth Data API
            response = requests.get(self.api_url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                data = response.json()  # Assuming the response is in JSON format

                # Extract relevant data from the response (modify as per your needs)
                # For example, if the JSON response has a 'data' key:
                extracted_data = data.get('data', [])

                # Save the data to a CSV file
                with open(self.output_csv, 'w', newline='') as csvfile:
                    fieldnames = []  # Define the fieldnames as per your data structure
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()

                    for item in extracted_data:
                        # Process and format the data as needed before writing to CSV
                        # Example: writer.writerow({'column1': item['field1'], 'column2': item['field2']})
                        pass

                print("Data scraped and saved to", self.output_csv)

                # Visualize the data as a pie chart or graph (optional)
                if self.output_image:
                    self.visualize_data(extracted_data)

            else:
                print("Failed to retrieve data. Status code:", response.status_code)

        except Exception as e:
            print("An error occurred:", str(e))

    def visualize_data(self, data):
        # Perform data visualization using Matplotlib (you can customize this)
        # Example: Create a pie chart
        labels = ['Category 1', 'Category 2', 'Category 3']  # Modify with your data categories
        sizes = [10, 30, 20]  # Modify with data values

        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.title('Data Distribution')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Save the visualization as an image
        plt.savefig(self.output_image)
        print("Data visualization saved as", self.output_image)

# Usage
if __name__ == "__main__":
    # Define the NASA Earth Data API URL you want to scrape data from
    api_url = "https://www.earthdata.nasa.gov/api-endpoint"

    # Define the output CSV file where the scraped data will be saved
    output_csv = "nasa_earth_data.csv"

    # Define the output image file for data visualization (optional)
    output_image = "data_visualization.png"

    # Create an instance of the scraper and initiate data scraping
    scraper = NasaEarthDataScraper(api_url, output_csv, output_image)
    scraper.scrape_data()
