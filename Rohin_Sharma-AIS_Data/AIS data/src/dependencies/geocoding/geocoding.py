import geocoder
import pandas as pd


class Geocoder:
    def __init__(self):
        return None

    def load_data(self, file_loc):
        data = pd.read_csv(file_loc)
        return data

    def get_coordinate(self, data):
        lat_long = None
        geo = geocoder.arcgis(data)
        lat_long = geo.latlng
        return lat_long

    def add_lat_long(self, data):
        data["Address"] = data["location"] + "," + data["country"]
        cod = data["Address"]
        cod = list(set(cod))
        Coordinate = [self.get_coordinate(cod) for cod in cod]
        Cords = pd.DataFrame(Coordinate, columns=["Latitude", "Longitude"])
        cod_data = pd.DataFrame(cod, columns=["Address"])
        result = pd.concat([cod_data, Cords], axis=1)
        result["Latitude"] = result["Latitude"].round(5)
        result["Longitude"] = result["Longitude"].round(5)
        data = data.merge(result, on="Address", how="left")
        data.drop(["Address"], axis=1, inplace=True)
        return data

    def add_lat_long_meta(self, data):
        data["Address"] = data["location"] + "," + data["country_name"]
        cod = data["Address"]
        cod = list(set(cod))
        Coordinate = [self.get_coordinate(cod) for cod in cod]
        Cords = pd.DataFrame(Coordinate, columns=["Latitude", "Longitude"])
        cod_data = pd.DataFrame(cod, columns=["Address"])
        result = pd.concat([cod_data, Cords], axis=1)
        result["Latitude"] = result["Latitude"].round(5)
        result["Longitude"] = result["Longitude"].round(5)
        data = data.merge(result, on="Address", how="left")
        data.drop(["Address"], axis=1, inplace=True)
        return data

    def save_data(self, data, filename):
        data.to_csv(filename, index=False)
        return None


if __name__ == "__main__":
    geocode = Geocoder()
    data = geocode.load_data("clean_ais_data.csv")
    geo_data = geocode.add_lat_long(data)
    geocode.save_data(geo_data, "final_ais_data.csv")
    m_data = geocode.load_data("ais_meta_data.csv")
    geo_data = geocode.add_lat_long_meta(m_data)
    geocode.save_data(geo_data, "ais_meta_data_geocoded.csv")
