from geopy.geocoders import Nominatim
import pandas as pd


class GeocodingRegion:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config")
        self.df = self.config['df']
        self.geolocator = Nominatim(user_agent="rajesh-PPP_Philippines")

    def geo_code(self):
        """geocoding region column if it is present"""
        location_label = []
        g_s_c = []
        for index, row in self.df.iterrows():
            try:
                if row['region'] != 'TBD':
                    pl = self.geolocator.geocode(str(row['region']) +
                                                 ', Philippines',
                                                 addressdetails=True)
                    if not pl:
                        address = row['region'].split('-')[0] + ', Philippines'
                        pl = self.geolocator.geocode(address,
                                                     addressdetails=True)
                    location_label.append(list(pl.raw['address'].values())[0])
                    g_s_c.append(f'{pl.latitude},{pl.longitude}')
                else:
                    location_label.append('TBD')
                    g_s_c.append('TBD')
            except KeyError:
                pass
        self.df['location_label'] = location_label
        self.df['geo_spatial_coordinates'] = g_s_c

    def run(self):
        """running geo_code function"""
        self.geo_code()
        return self.df


if __name__ == "__main__":
    config = {'df': pd.DataFrame()}
    obj = GeocodingRegion(config=config)
    obj.run()
