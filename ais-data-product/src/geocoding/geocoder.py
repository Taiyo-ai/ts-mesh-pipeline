from cleaning import cleaner
import pandas as pd
import reverse_geocode
from cleaning import cleaner
from geopy.geocoders import Nominatim
import geopy.geocoders as gg
import ssl

def transformed()->pd.DataFrame:
    """ This function will find the nearest city 
        according to the latitude and longitude
    """
    dfclean = cleaner.dataCleaner()
    lat = dfclean['Latitude']
    lng = dfclean['Longitude']
    nearest_city = []
    city_list = []
    state_list = []
    pin_code_list = []
    district_list = []
    for x , y in zip(lat , lng):
        if x == 0.0 and y == 0.0:
            continue
        cordinates = (x , y),
        city = reverse_geocode.search(cordinates)
        city = city[0]['city']
        nearest_city.append(city)
        

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        gg.options.default_ssl_context = ctx
        
        location =  Nominatim(user_agent="Tausif").reverse(str(x) + ","+ str(y),timeout=20)
        try:
            address = location.raw['address']

            city = address.get('city','' )
            city_list.append(city)

            district = address.get('state_district', '')
            district_list.append(district)
            
            state = address.get('state', '')
            state_list.append(state)

            pin_code = address.get('postcode','' )
            pin_code_list.append(pin_code)

        except Exception:
            pass
    
    dfclean['nearest_city'] = pd.DataFrame(nearest_city)
    
    dfclean['city'] = pd.DataFrame(city_list)

    dfclean['district'] = pd.DataFrame(district_list)

    dfclean['state'] = pd.DataFrame(state_list)

    dfclean['postcode'] = pd.DataFrame(pin_code_list)

    
    return dfclean
    