# Time Series Data

import os 
import datetime 
import time
import requests 
import urllib.request 
from bs4 import BeautifulSoup 
import re 
import json
import pandas as pd 
import zipfile as zp


#Apple

def get_apple_link():
# get link via API
json_link = "https://covid19-static.cdn-apple.com/covid19-mobility-data/current/v3/index.json"
with urllib.request.urlopen(json_link) as url:
    json_data = json.loads(url.read().decode())
link = "https://covid19-static.cdn-apple.com" + \
    json_data['basePath'] + json_data['regions']['en-us']['csvPath']
return link

def download_apple_report(directory="apple_reports"): 
# create directory if it don't exist
if not os.path.exists(directory) and directory!='':
    os.makedirs(directory)

link = get_apple_link()
file_name = "applemobilitytrends.csv"
path = os.path.join(directory, file_name)
path = os.path.join(directory, file_name)
old_size = os.path.getsize(path) if os.path.isfile(path) else 0
urllib.request.urlretrieve(link, path)
new_size = os.path.getsize(path)
if old_size!=new_size:
    new_files = True

if not new_files:
    print('Apple: No updates')
else:
    print('Apple: Update available')

return new_files

def build_apple_report( source=os.path.join( 'apple_reports', "applemobilitytrends.csv"), report_type="regions"): 
apple = pd.read_csv(source, low_memory=False)
apple = apple.drop(columns=['alternative_name'])
apple['country'] = apple.apply(
    lambda x: x['region'] if x['geo_type'] == 'country/region' else x['country'],
    axis=1)

if report_type == 'regions':
    apple = apple[apple.geo_type != 'county']
    apple['sub-region'] = apple.apply(lambda x: 'Total' if x['geo_type'] == 'country/region' else (
        x['region'] if x['geo_type'] == 'sub-region' else x['sub-region']), axis=1)
    apple['subregion_and_city'] = apple.apply(
        lambda x: 'Total' if x['geo_type'] == 'country/region' else x['region'], axis=1)
    apple = apple.drop(columns=['region'])
    apple['sub-region'] = apple['sub-region'].fillna(
        apple['subregion_and_city'])

    apple = apple.melt(
        id_vars=[
            'geo_type',
            'subregion_and_city',
            'sub-region',
            'transportation_type',
            'country'],
        var_name='date')
    apple['value'] = apple['value'] - 100

    apple = apple.pivot_table(
        index=[
            "geo_type",
            "subregion_and_city",
            "sub-region",
            "date",
            "country"],
        columns='transportation_type').reset_index()
    apple.columns = [t + (v if v != "value" else "")
                     for v, t in apple.columns]
    apple = apple.loc[:,
                      ['country',
                       'sub-region',
                       'subregion_and_city',
                       'geo_type',
                       'date',
                       'driving',
                       'transit',
                       'walking']]
    apple = apple.sort_values(by=['country',
                                  'sub-region',
                                  'subregion_and_city',
                                  'date']).reset_index(drop=True)
elif report_type == "US":
    apple = apple[apple.country == "United States"].drop(columns=[
                                                         'country'])
    apple['sub-region'] = apple['sub-region'].fillna(
        apple['region']).replace({"United States": "Total"})
    apple['region'] = apple.apply(lambda x: x['region'] if (
        x['geo_type'] == 'city' or x['geo_type'] == 'county') else 'Total', axis=1)
    apple = apple.rename(
        columns={
            'sub-region': 'state',
            'region': 'county_and_city'})

    apple = apple.melt(
        id_vars=[
            'geo_type',
            'state',
            'county_and_city',
            'transportation_type'],
        var_name='date')
    apple['value'] = apple['value'] - 100

    apple = apple.pivot_table(
        index=[
            'geo_type',
            'state',
            'county_and_city',
            'date'],
        columns='transportation_type').reset_index()
    apple.columns = [t + (v if v != "value" else "")
                     for v, t in apple.columns]

    apple = apple.loc[:, ['state', 'county_and_city', 'geo_type',
                          'date', 'driving', 'transit', 'walking']]
    apple = apple.sort_values(
        by=['state', 'county_and_city', 'geo_type', 'date']).reset_index(drop=True)
return apple




# Google

def get_google_link(): 
# get webpage source
url = 'https://www.google.com/covid19/mobility/'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
csv_tag = soup.find('a', {"class": "icon-link"})
link = csv_tag['href']
return link

def download_google_report(directory="google_reports"):
new_files = False

# create directory if it don't exist
if not os.path.exists(directory) and directory!='':
    os.makedirs(directory)

# download CSV file
link = get_google_link()
file_name = "Global_Mobility_Report.csv"
path = os.path.join(directory, file_name)
old_size = os.path.getsize(path) if os.path.isfile(path) else 0
urllib.request.urlretrieve(link, path)
new_size = os.path.getsize(path)
if old_size!=new_size:
    new_files = True

if not new_files:
    print('Google: No updates')
else:
    print('Google: Update available')

return new_files

def build_google_report( source=os.path.join("google_reports", "Global_Mobility_Report.csv"), report_type="regions", countries=None, world_regions=None, country_regions_file = os.path.join("auxiliary_data", "country_worldregions.csv")):
# read the raw report
google = pd.read_csv(source, low_memory=False)
# shorten value column names
google.columns = google.columns.str.replace(
    r'_percent_change_from_baseline', '')
# remove underscores from column names
google.columns = google.columns.str.replace(r'_', ' ')
# rename country column
google = google.rename(columns={'country region': 'country'})
if report_type == "regions":
    # remove data of subregions of the second level
    google = google[google['sub region 2'].isnull()]
    # remove metropolitan data
    google = google[google['metro area'].isnull()]
    # rename region column
    google = google.rename(columns={'sub region 1': 'region'})
    google = google.loc[:,
                        ['country',
                         'region',
                         'date',
                         'retail and recreation',
                         'grocery and pharmacy',
                         'parks',
                         'transit stations',
                         'workplaces',
                         'residential']]
    google['region'].fillna('Total', inplace=True)
elif report_type == "US":
    google = google[(google['country'] == "United States")]
    google = google.rename(
        columns={
            'sub region 1': 'state',
            'sub region 2': 'county'})
    google = google.loc[:,
                        ['state',
                         'county',
                         'date',
                         'retail and recreation',
                         'grocery and pharmacy',
                         'parks',
                         'transit stations',
                         'workplaces',
                         'residential']]
    google['state'].fillna('Total', inplace=True)
    google['county'].fillna('Total', inplace=True)
elif report_type == "regions_detailed" or report_type == "world_regions_detailed":
    if countries is not None and report_type == "regions_detailed":
        google = google[google.country.isin(countries)]
    if report_type == "world_regions_detailed":
        if os.path.isfile(country_regions_file):
            country_regions = pd.read_csv(country_regions_file)
        google = pd.merge(google, country_regions, on='country')
        if world_regions is not None:
            google = google[google.world_region.isin(world_regions)]
    # metro area -> sub region 1    
    google['sub region 1'] = google.apply(lambda x: x['sub region 1'] if isinstance(x['sub region 1'],str)
                                              else x['metro area'], axis=1)
    column_list = ['world_region'] if report_type == "world_regions_detailed" else []
    column_list = column_list + ['country',
                     'sub region 1',
                     'sub region 2',
                     'date',
                     'retail and recreation',
                     'grocery and pharmacy',
                     'parks',
                     'transit stations',
                     'workplaces',
                     'residential']
    google = google.loc[:, column_list]
    google['sub region 1'].fillna('Total', inplace=True)
    google['sub region 2'].fillna('Total', inplace=True)
return google