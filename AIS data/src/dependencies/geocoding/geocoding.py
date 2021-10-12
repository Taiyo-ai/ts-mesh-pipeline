from geopy.geocoders import Nominatim
import pandas as pd

geolocator = Nominatim(user_agent="my_user_agent")


class Geocoder:
    def __init__(self):
        return None

    def load_data(self, file_loc):
        data = pd.read_csv(file_loc)
        return data

    def add_lat_long(self, data):
        lat = []
        long = []
        for i in range(len(data)):
            loc = geolocator.geocode(data["location"][i] + "," + data["country"][i])
            if loc != None:
                lat.append(loc.latitude)
                long.append(loc.longitude)
            else:
                lat.append("Nil")
                long.append("Nil")
        data["latitude"] = lat
        data["longitude"] = long
        return data

    def save_data(self, data, filename):
        data.to_csv(filename, index=False)
        return None


if __name__ == "__main__":
    geocode = Geocoder()
    data = geocode.load_data("clean_ais_data.csv")
    geo_data = geocode.add_lat_long(data)
    geocode.save_data("ais_data_geocoded.csv")
