#!/usr/bin/env python
# coding: utf-8

# ## 2. BIS
# • Get the list of the all datasets and respective links from the below mentioned URL source and store it into a csv file.
# • Create a scraper to get “Credit-to-GDP-gaps” dataset from the same source. The Scraper must be a python class.
# • Store the data in a CSV format with a Timestamp and each country as a sperate column. The original source has timeseries as horizontal axis.
# Link: https://www.bis.org/statistics/full_data_sets.htm

# NOTE :  I tried to clear doubt regarding the exact meaning the sentences want to convey but there was no response. Hope I have interpreted them correctly

# importing necessary libraries
import requests
from bs4 import BeautifulSoup
import io
from csv import writer
from PyPDF2 import PdfFileReader

# website to scrap
url = "https://www.bis.org/statistics/full_data_sets.htm"
 
# get the url from requests get method
read = requests.get(url)
 
# full html content
html_content = read.content
 
# Parse the html content
soup = BeautifulSoup(html_content, "html.parser")

# importing necessary libraries
from io import BytesIO
from zipfile import ZipFile
import pandas as pd

# getting the dataset and their links
with open('datasets.csv','w', encoding = 'utf8',newline = '') as fi:
    thewriter = writer(fi)
    label = ["Datasets", "URL"]
    thewriter.writerow(label)
    #Find all the links on the page that end in .zip and write them into the text file
    for anchor in soup.find_all('a', href=True):
        links = anchor['href']
        if links.endswith('.zip'):
            link = ("https://www.bis.org/" + links + '\n')
            name = anchor.get_text()
            info = [name, link]
            thewriter.writerow(info)

# scraper to read the "Credit-to-GDP gaps" dataset 
for anchor in soup.find_all('a', href=True):
        if anchor['href'].endswith('.zip'):
            if anchor.get_text() =="Credit-to-GDP gaps":
                newlink = ("https://www.bis.org/" + anchor['href'] )
                content = requests.get(newlink)
                
                zf = ZipFile(BytesIO(content.content)) 
                match = [s for s in zf.namelist() if ".csv" in s][0]
                file = zf.open(match)
#                 with open(match +'.csv','w') as output_file:
#                     output_file.write(file)
                df = pd.read_csv(file)


df_new = df.drop(['Frequency', 'Borrowing sector', 'Lending sector',
       'Credit gap data type', 'Title (tseries level)', 'Time Period'], axis=1)

df_t = df_new.T
#df_t.fillna("NA")
#df_t

import datetime
#print(datetime.datetime.now())
new_header = df_t.iloc[0] #grab the first row for the header
df_col = df_t[1:] #take the data less the header row
df_col.columns = new_header #set the header row as the df header
df_col['Timestamp'] = datetime.datetime.now()
#df_col

# Export the final dataframe to csv
df_col.to_csv("Transformed_Credit-to-GDP_gaps.csv")

