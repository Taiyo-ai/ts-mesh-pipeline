import pandas as pd
import os
from datetime import datetime
import country_converter as cc
import reverse_geocode
from geopy.geocoders import Nominatim
from geocoding import geocoder

def dataCleaner()->pd.DataFrame:
    """
    This function cleans the data from the dataset.
    :return: Cleaned dataframe
    """
    # Read the dataset
    df = pd.read_csv("../../data/ScrappedData.csv")

    #copying the dataframe
    dfclean = df.copy()
    
    #Checking null values ..
    dfclean.isnull().sum()
    
    dfclean['station_ID'] = dfclean['ID']
    
    #converting the country code from alpha2 to alpha3 and replacing unknown location with unknown
    dfclean['country_code'] =  dfclean['Country']\
        .apply(lambda x : cc.convert(names=x, to='ISO3',not_found='unknown') )
    
    # Region name filter
    dfclean['region_name'] = dfclean['Location'].\
    apply(lambda x : (x.split()[0] +' ' + x.split()[1]) if len(x.split())>2 else x)
        
    #findind location for zero latitude and longitude
    unknown_location = dfclean.loc[dfclean['Latitude']==0.00 ]
    
    def fillingZero(dfclean)->pd.DataFrame:
        """Filling zero lat and long with city cordinate  """
        city_list = []
        for i in unknown_location['Location']:
            if i == 'At Sea':
                continue
            else:
                city_list.append(i)

        for i in city_list:
            try:
                index = dfclean[dfclean['Location']== i].index.values
                #extracting latitude
                lat = Nominatim(user_agent="Tausif").geocode(i , timeout=20).latitude
                #replacing in rows having zero cordinate
                dfclean.at[index,'Latitude']=lat

                #extracting longitude
                lng = Nominatim(user_agent="Tausif").geocode(i , timeout=20).longitude
                #replacing in rows having zero cordinate
                dfclean.at[index,'Longitude'] = lng
            
            except Exception:
                pass
        return dfclean
    
    dfclean = fillingZero(dfclean)
    
    def regionCode(dfclean)->pd.DataFrame:
        """ Extracting region code """
        region = []
        for x,y in zip(dfclean['region_name'] ,dfclean['country_code']) :

            if len(x.split())>1:
                x = x.split()[0:2]
                x = x[0][0] + x[1][0] + ' , ' + y
                region.append(x)
            else:
                x = x[0:2].upper() + ' , ' + y
                region.append(x)
                dfclean['region_code'] = pd.DataFrame(region)
        return dfclean
    dfclean = regionCode(dfclean)
    
    #dropping rows having no regions or wherebouts
    no_region = dfclean.loc[dfclean['Latitude'] == 0.00 ]
    index_name = no_region.index
    dfclean.drop(index_name , inplace= True)
     
    #Calling geocoder function for finding location  
    return dfclean
    
    
    