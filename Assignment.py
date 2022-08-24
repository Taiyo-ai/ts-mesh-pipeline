#!/usr/bin/env python
# coding: utf-8

# In[7]:


from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd


# In[32]:


import requests

res = requests.get('https://www.bea.gov/')

print(res.text)
print(res.status_code)


# In[38]:


import requests

# Make a request to https://codedamn-classrooms.github.io/webscraper-python-codedamn-classroom-website/
# Store the result in 'res' variable
res = requests.get(
    'https://developer.taiyo.ai/api-doc/TimeSeries/')
txt = res.text
status = res.status_code

print(txt, status)
# print the result


# In[40]:


from bs4 import BeautifulSoup

page = requests.get("https://www.bea.gov/")
soup = BeautifulSoup(page.content, 'html.parser')
title = soup.title.text # gets you the text of the <title>(...)</title>
print(title)


# In[41]:


import requests
from bs4 import BeautifulSoup

# Make a request to https://codedamn-classrooms.github.io/webscraper-python-codedamn-classroom-website/
page = requests.get(
    "https://developer.taiyo.ai/api-doc/TimeSeries/")
soup = BeautifulSoup(page.content, 'html.parser')

# Extract title of page
page_title = soup.title.text

# print the result
print(page_title)


# In[42]:


import requests
from bs4 import BeautifulSoup

# Make a request
page = requests.get(
    "https://www.bea.gov/")
soup = BeautifulSoup(page.content, 'html.parser')

# Extract title of page
page_title = soup.title.text

# Extract body of page
page_body = soup.body

# Extract head of page
page_head = soup.head

# print the result
print(page_body, page_head)


# In[43]:


import requests
from bs4 import BeautifulSoup

# Make a request
page = requests.get(
    "https://developer.taiyo.ai/api-doc/TimeSeries/")
soup = BeautifulSoup(page.content, 'html.parser')

# Extract title of page
page_title = soup.title

# Extract body of page
page_body = soup.body

# Extract head of page
page_head = soup.head

# print the result
print(page_title, page_head)


# In[44]:


import requests
from bs4 import BeautifulSoup

# Make a request
page = requests.get(
    "https://developer.taiyo.ai/api-doc/TimeSeries/")
soup = BeautifulSoup(page.content, 'html.parser')

# Extract first <h1>(...)</h1> text
first_h1 = soup.select('h1')[0].text
print(first_h1)


# In[45]:


import requests
from bs4 import BeautifulSoup
# Make a request
page = requests.get(
    "https://developer.taiyo.ai/api-doc/TimeSeries/")
soup = BeautifulSoup(page.content, 'html.parser')

# Create all_h1_tags as empty list
all_h1_tags = []

# Set all_h1_tags to all h1 tags of the soup
for element in soup.select('h1'):
    all_h1_tags.append(element.text)

# Create seventh_p_text and set it to 7th p element text of the page
seventh_p_text = soup.select('p')[6].text

print(all_h1_tags, seventh_p_text)


# In[47]:


info = {
   "title": 'Asus AsusPro Adv...   '.strip(),
   "review": '2 reviews\n\n\n'.strip()
}


# In[49]:


import requests
from bs4 import BeautifulSoup
# Make a request
page = requests.get(
    "https://developer.taiyo.ai/api-doc/TimeSeries/")
soup = BeautifulSoup(page.content, 'html.parser')

# Create top_items as empty list
top_items = []

# Extract and store in top_items according to instructions on the left
products = soup.select('div.thumbnail')
for elem in products:
    title = elem.select('h4 > a.title')[0].text
    review_label = elem.select('div.ratings')[0].text
    info = {
        "title": title.strip(),
        "review": review_label.strip()
    }
    top_items.append(info)

print(top_items)


# In[51]:


import requests
from bs4 import BeautifulSoup
# Make a request
page = requests.get(
    "https://developer.taiyo.ai/api-doc/TimeSeries/")
soup = BeautifulSoup(page.content, 'html.parser')

# Create top_items as empty list
image_data = []

# Extract and store in top_items according to instructions on the left
images = soup.select('img')
for image in images:
    src = image.get('src')
    alt = image.get('alt')
    image_data.append({"src": src, "alt": alt})

print(image_data)


# In[52]:


info = {
   "href": "<link here>",
   "text": "<link text here>"
}


# In[53]:


import requests
from bs4 import BeautifulSoup
# Make a request
page = requests.get(
    "https://developer.taiyo.ai/api-doc/TimeSeries/")
soup = BeautifulSoup(page.content, 'html.parser')

# Create top_items as empty list
all_links = []

# Extract and store in top_items according to instructions on the left
links = soup.select('a')
for ahref in links:
    text = ahref.text
    text = text.strip() if text is not None else ''

    href = ahref.get('href')
    href = href.strip() if href is not None else ''
    all_links.append({"href": href, "text": text})

print(all_links)


# In[57]:


import requests
from bs4 import BeautifulSoup
import csv
# Make a request
page = requests.get(
    "https://developer.taiyo.ai/api-doc/TimeSeries/")
soup = BeautifulSoup(page.content, 'html.parser')

# Create top_items as empty list
all_products = []

# Extract and store in top_items according to instructions on the left
products = soup.select('div.thumbnail')
for product in products:
    name = product.select('h4 > a')[0].text.strip()
    description = product.select('p.description')[0].text.strip()
    price = product.select('h4.price')[0].text.strip()
    reviews = product.select('div.ratings')[0].text.strip()
    image = product.select('img')[0].get('src')

    all_products.append({
        "name": name,
        "description": description,
        "price": price,
        "reviews": reviews,
        "image": image
    })


keys = all_products[0].keys()

with open('products.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(all_products)

