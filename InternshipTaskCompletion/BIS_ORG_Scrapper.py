import os
import requests
import pandas as pd
import wget
import zipfile
from datetime import datetime
from bs4 import BeautifulSoup
from constants import *


class BIS_Scrapper:
    def __init__(self,base_url:str,endpoint:str):
        self.base_url = base_url
        self.endpoint = endpoint
        self.scrapper.__call__()

    def scrapper(self):
        try:
            page_content = requests.get(self.base_url + self.endpoint)
            scrap_content = BeautifulSoup(page_content.content, "html.parser")
            dataset_data = [{"dataset":ele.text,"url":self.base_url + str(ele.attrs.get("href"))} for ele in scrap_content.find("div",id="cmsContent").find("ul").find_all("a") ]
            dataset_data = pd.DataFrame(dataset_data)
            dataset_data.to_csv("dataset_csv.csv")
            credit2GDP_gap_url = dataset_data[dataset_data["dataset"] == "Credit-to-GDP gaps"]["url"].values[0]
            print(f"Printing File Name : {credit2GDP_gap_url}")
            file_download_path = wget.download(credit2GDP_gap_url)
            print(f"Printing Download zip file path {file_download_path}")
            downloded_zipfile = zipfile.ZipFile(os.getcwd() +"\\" + file_download_path)
            downloded_zipfile.extractall(os.getcwd())
            country_wise_data = pd.DataFrame()
            credit_GDP_dataset = pd.read_csv(r"C:\Users\HC117BC\Downloads\Taiyo\WS_CREDIT_GAP_csv_col.csv")
            country_wise_data["country"] = credit_GDP_dataset["Borrowers' country"]
            country_wise_data["Time_Stamp"] = datetime.now()
            country_wise_data.to_csv("country_wise_data.csv")
        except Exception as e:
            print(f"Exception Occurred : {e}")








if __name__ == "__main__":
    BIS_Scrapper(BIS_BASEURL,BIS_ENDPOINT)