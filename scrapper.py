from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
import ee
# ee.Authenticate()
import pandas as pd


class Scrapper:
    def scrap(self):
        lc = ee.ImageCollection('MODIS/006/MCD12Q1')

        # Import the MODIS land surface temperature collection.
        lst = ee.ImageCollection('MODIS/006/MOD11A1')

        # Import the USGS ground elevation image.
        elv = ee.Image('USGS/SRTMGL1_003')

        # Initial date of interest (inclusive).
        i_date = '2020-01-01'

        # Final date of interest (exclusive).
        f_date = '2022-01-01'

        # Selection of appropriate bands and dates for LST.
        lst = lst.select('LST_Day_1km', 'QC_Day').filterDate(i_date, f_date)
        # Define the urban location of interest as a point near Washington, USA.

        u_lon = 120.7401
        u_lat = 47.7511
        u_poi = ee.Geometry.Point(u_lon, u_lat)
        scale = 1000  # scale in meters

        # Print the elevation near Lyon, France.
        elv_urban_point = elv.sample(
            u_poi, scale).first().get('elevation').getInfo()
        print('Ground elevation at urban point:', elv_urban_point, 'm')

        # Calculate and print the mean value of the LST collection at the point.
        lst_urban_point = lst.mean().sample(
            u_poi, scale).first().get('LST_Day_1km').getInfo()
        print('Average daytime LST at urban point:', round(
            lst_urban_point*0.02 - 273.15, 2), '°C')

        # Print the land cover type at the point.
        lc_urban_point = lc.first().sample(u_poi, scale).first().get('LC_Type1').getInfo()
        print('Land cover value at urban point is:', lc_urban_point)


Sc = Scrapper()
Sc.scrap()
