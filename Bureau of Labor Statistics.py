#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import seaborn as sns


# In[2]:


#Importing Url
url = "https://www.bls.gov/eag/eag.us.htm"    #open link
html = urlopen(url)


# In[3]:


soup = BeautifulSoup(html)


# In[4]:


title = soup.title
print(title)
print(title.text)


# In[5]:


links = soup.find_all('a', href=True)
for link in links:
    print(link['href'])


# In[6]:


data = []
allrows = soup.find_all("tr")
for row in allrows:
    row_list = row.find_all("td")
    dataRow = []
    for cell in row_list:
        dataRow.append(cell.text)
    data.append(dataRow)
data = data[1:]
print(data[-2:])


# In[7]:


df = pd.DataFrame(data)
print(data)


# In[8]:


df = pd.DataFrame(data)
print(df.head())
print(df.tail())


# In[9]:


df.head()


# In[10]:


header_list =[]
col_headers = soup.find_all('th')
for col in col_headers:
    header_list.append(col.text)
print(header_list)


# In[11]:


df.columns = ['Data Series','June 2022','July 2022','Aug 2022','Sept 2022','Oct 2022','Nov 2022']


# In[12]:


df.info()


# In[13]:


df.shape


# In[14]:


df.describe()


# In[15]:


df.rows = ['Data Series','Unemployment Rate(1)','Change in Payroll Employment(2)','Average Hourly Earnings(3)','Consumer Price Index(4)','Producer Price Index(5)','U.S. Import Price Index(6)','(7)','(8)','(9)','(10)']


# In[16]:


df.head()


# In[17]:


df.rows


# In[18]:


#Saving output to csv file
df.to_csv(r'C:/Users/user/Dropbox/PC/Desktop/Machine Learning/Taiyo/web scrapping/BLS.csv', index = False, header = True)


# In[19]:


df = pd.read_csv("BLS.csv")


# In[20]:


df.head()


# In[ ]:




