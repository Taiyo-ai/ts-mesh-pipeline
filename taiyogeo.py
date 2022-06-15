import ee #pip install earthengine-api #install gcloud
import csv
from geopy.geocoders import Nominatim #pip install geopy
from datetime import date, timedelta

ee.Initialize()

class myee:
    def run(self):
        scale = 1000

        address = input("Enter location : ")
        geolocator = Nominatim(user_agent="my_user_agent") #Converting Location to Latitude and Longitude
        loc = geolocator.geocode(address)
        poi = ee.Geometry.Point(loc.longitude, loc.latitude)

        start_date = date(2021, 6, 10) # Start Date for range
        end_date = date(2022, 6, 10) # End Date for range
        delta = timedelta(days=1)
        while start_date <= (end_date):

            try:
                i_date = str(start_date) 
                f_date = str(start_date + delta)

                lst = ee.ImageCollection('MODIS/006/MOD11A1') #Image Collection for Land Surface Temperature
                lc = ee.ImageCollection('MODIS/006/MCD12Q1') #Image Collection for Land Cover

                lst = lst.select('LST_Day_1km', 'QC_Day').filterDate(i_date, f_date) #Selecting required band from Image Collection

                lst_point = lst.mean().sample(poi, scale).first().get('LST_Day_1km').getInfo()

                lc_point = lc.first().sample(poi, scale).first().get('LC_Type1').getInfo()

                list_csv = list() #Empty list to append to csv file

                list_csv.append(address)
                list_csv.append(start_date)
                list_csv.append(round(lst_point*0.02 -273.15, 2)) # Converting to C
                list_csv.append(lc_point)

                with open('data.csv', 'a', encoding='UTF8', newline='') as f: #create file named data.csv for output
                    writer = csv.writer(f)

                    writer.writerow(list_csv)
            
                start_date += delta
            
            except:

                start_date += delta
                
                continue

x = myee()

x.run()

#end