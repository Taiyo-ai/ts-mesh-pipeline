#!/usr/bin/env python
# coding: utf-8

# In[11]:


class DataLoader():
    
    def __init__(self, path, webdr_loc):
        self.webdr_loc = webdr_loc
        self.path = path

    def load_module(self):

        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import csv
        import pdb
        import pandas as pd
        import time

        # Headless mode
        options = Options()  # Initialize an instance of the Options class
        options.headless = True  # True -> Headless mode activated
        options.add_argument('window-size=1920x1080')  # Set a big window size, so all the data will be displayed


        website = self.path
        path = self.webdr_loc
        driver = webdriver.Chrome(path,options=options)
        driver.get(website)
        # driver.maximize_window()

        elem = driver.find_element(By.XPATH, '//a[contains(@href, "event-search")]')
        new_path = elem.get_attribute("href")

        driver.quit()

        website = new_path
        path = self.webdr_loc
        #r'C:\Users\vempa\OneDrive\Desktop\Abhi\Intershala_DataScience\Interview - Final\web scrapping\Udemy-course\chromedriver'
        driver = webdriver.Chrome(path,options=options)
        driver.get(website)

        records = []

        projects_list = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id = "dtDrop"]//tbody//tr')))

        for project in projects_list:
        #     pdb.set_trace()
            eventid = project.find_element(By.XPATH,'.//td[2]').text
            Ename = project.find_element(By.XPATH,'.//td[3]').text
            Dname = project.find_element(By.XPATH,'.//td[4]').text
            Edate = project.find_element(By.XPATH,'.//td[5]').text
            status = project.find_element(By.XPATH,'.//td[6]').text

            records.append((eventid, Ename, Dname, Edate, status))

        df_cal_projects = pd.DataFrame(records, columns=['Event ID','Event Name', 'Dept Name','End Date','Status']) 
        driver.quit()
        df_cal_projects.to_csv('file1.csv', index = False)




