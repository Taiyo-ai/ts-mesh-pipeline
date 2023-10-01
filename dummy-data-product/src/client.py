# import your dependencies here
import csv

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


class MyClass:
    def __init__(self, url):
        self.url = url

    @staticmethod
    def scrap(result, keytype, param, data):
        for i in data:
            if i.get(param) and len(i.get(param)) > 1:
                temp = [keytype, i.get(param)]
                result.append(temp)

    def extract_data(self, soup):
        """Do extraction or processing of data here"""

        scraped_data = []
        self.scrap(scraped_data, "Link", "href", soup.find_all('a'))
        self.scrap(scraped_data, "Divclassnames", "class", soup.find_all('div'))
        self.scrap(scraped_data, "Divids", "id", soup.find_all('div'))

        return scraped_data

    def load_data(self):
        """Function to load data"""
        url = self.url

        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, "html.parser")
            return self.extract_data(soup)
        else:
            print("Failed to retrieve the page. Status code:", response.status_code)

        return None

    def save_data(self, scraped_data):
        """Function to save data"""
        csv_file_name = "output_data.csv"

        # Save the data to a CSV file
        with open(csv_file_name, mode='w', newline='') as csv_file:
            fieldnames = ['Keys', 'Values']
            writer = csv.writer(csv_file)

            # Write the header row
            writer.writerow(fieldnames)
            # Write the data rows
            writer.writerows(scraped_data)

        print(f"Data saved to {csv_file_name}")
        return None

    def run(self):
        """Load data, do_something and finally save the data"""
        loaded_data = self.load_data()
        self.save_data(loaded_data)
        return None


def getdatainfo(data_number):
    if data_number == '1':
        data_url = "https://www.earthdata.nasa.gov/engage/open-data-services-and-software/api"
    elif data_number == '2':
        data_url = "https://www.nnvl.noaa.gov/view/globaldata.html"
    elif data_number == '3':
        data_url = "https://www.bea.gov/"
    elif data_number == '4':
        data_url = "https://www.datacommons.org/"
    else:
        data_url = ""

    return data_url


if __name__ == "__main__":
    data_chosen = input("Select the data you want to scrap from the below list:\n"
                        "1. Nasa Earth Data\n2. NOAA World Data\n3. Bureau of Economic Analysis\n4. Google Data Commons\n"
                        "Enter your chosen number: ")

    url = getdatainfo(data_chosen)
    obj = MyClass(url)
    obj.run()
