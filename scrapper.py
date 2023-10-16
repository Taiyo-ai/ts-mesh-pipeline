import selenium
import pandas as pd
from selenium import webdriver
import warnings
warnings.filterwarnings("ignore")
import time

def scrape_data_from_page(driver):
    headings = []
    text_before_hyphen = []
    text_after_hyphen = []

    h = driver.find_elements(by='xpath', value="//h3[@class='Content Type : Reports title']")
    for j in h:
        heading_text = j.text
        headings.append(heading_text)
        parts = heading_text.split(' - ')
        if len(parts) == 2:
            text_before_hyphen.append(parts[0])
            text_after_hyphen.append(parts[1])

    return headings, text_before_hyphen, text_after_hyphen
