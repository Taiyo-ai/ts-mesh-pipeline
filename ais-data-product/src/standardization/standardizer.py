
from io import FileIO
import pandas as pd
from geocoding import geocoder
from datetime import datetime


def dataStandardizer()->FileIO:
    """
    This function standardizes the data by removing the columns that are not
    needed and then renaming the columns to be more readable.
    """
    # Remove the columns that are not needed
    #Converting unix time into date time object
    dfclean = geocoder.transformed()
    dfclean['last_signal'] = pd.to_datetime(dfclean['Last signal'],unit = 's')
    # Duration of signal from current time
    #dfclean['Total_dur_since_last_signal'] = dfclean['last_signal'].\
        #apply(lambda x : datetime.now()- x)
    
    dfclean.drop(['Country','Latitude','Longitude','ID','Location' , 'Last signal'],\
        axis = 1 , inplace= True)
    # sea locations or unknown
    
    dfclean.to_csv('../../data/Transformed_Data.csv')
    
    
    
    