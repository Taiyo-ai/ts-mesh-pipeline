from geopy.geocoders import Nominatim
import re
import pandas as pd


class CSVConverter:
    def __init__(self, csv_file, address_column):
        self.csv_file = csv_file
        self.address_column = address_column
        self.geolocator = Nominatim(user_agent="my_geocoder")

    def get_location(self, address):
        address = re.sub(r'([A-Z][A-z]+)([A-Z][A-z]+)', r'\2, \1', address)
        print(address)

        # Geocode the address
        location = self.geolocator.geocode(address)

        if location:
            latitude = location.latitude
            longitude = location.longitude
            return (latitude, longitude)
        else:
            print(f"Unable to retrieve coordinates for the address: {address}")
            return None

    def get_coordinates(self):
        df = pd.read_csv(self.csv_file)
        df['geo_fields'] = df[self.address_column].apply(lambda c: self.get_location(c))
        print(df['geo_fields'])
        df['latitude'] = df['geo_fields'].apply(lambda gf: gf[0] if gf else '')
        df['longitude'] = df['geo_fields'].apply(lambda gf: gf[1] if gf else '')
        df.drop(columns=['geo_fields'], inplace=True)
        df.to_csv('geocoder.csv', index=False)


