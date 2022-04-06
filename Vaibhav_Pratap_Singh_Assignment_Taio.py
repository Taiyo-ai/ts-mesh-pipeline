#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Web scrapper code and fetching relavant data for further working
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import pandasql as ps
import csv
url=requests.get("https://covid19.apple.com/mobility.com")
soup=BeautifulSoup(url.content, "html.parser")
links=soup.find_all('a')
all_links=[]
for link in links:
    all_links.append(link.get('href'))
datalink="https://covid19-static.cdn-apple.com/covid19-mobility-data/2211HotfixDev7/v3/en-us/applemobilitytrends-2022-03-31.csv"
data=pd.read_csv(datalink,low_memory=False)
print(data)


# In[2]:


# Checking the accessibility of sql and forming sample table for same
finalTable = ps.sqldf("select region,`2020-01-13` as '13Jan2020',`2020-01-14` as '14Jan2020',`2020-01-15` as '15Jan2020',`2020-01-16` as '16Jan2020',`2020-01-17` as '17Jan2020' from data limit 4000")
finalTable


# In[3]:


#using melt function to transpose the data from coloumn to row
finalTable1 = finalTable.melt(id_vars=['region'],var_name = 'date', value_name = 'casesCount')
finalTable1


# In[5]:


#Using sql queries to Get Daily casescount of top 50 Regions.
final2 = ps.sqldf("select region,date, casesCount,  dn as MyRank from (select region,date, casesCount, dense_rank() over(partition by date order by casesCount desc) as dn from finalTable1 order by date desc) temp where dn <=50")
final2


# In[6]:


#Converting the result of sql query as dataframe and saving it as csv file
data_frame = pd.DataFrame(final2)
data_frame.to_csv('final_output.csv')


# In[7]:


#Reading Saved output final
df=pd.read_csv("final_output.csv")
print(df.head(500))


# In[143]:


# To Display date wise covid cases 
from dateutil.parser import parse 
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
series_value=cases.values

cases=pd.read_csv('final_output.csv',usecols=['date','casesCount'])
case=cases.dropna(axis=0)
print(case)


# In[144]:


#Getting datewise aggregated value of cases 
Daywise_count = case.groupby('date')['casesCount'].sum()
Daily_count=Daywise_count.tail(n=4)
print(Daily_count)


# In[146]:


# Displaying datewise total no of cases
Daily_count.plot(title='Date wise covid cases')


# In[ ]:




