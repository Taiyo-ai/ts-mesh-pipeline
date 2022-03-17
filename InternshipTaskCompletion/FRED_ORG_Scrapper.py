import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from constants import *


class FRED_Scrapper:
    def __init__(self,base_url:str,endpoint:str):
        self.base_url = base_url
        self.endpoint = endpoint
        self.scrapper.__call__()

    def scrapper(self):
        try:
            page_content = requests.get(self.base_url + self.endpoint)
            scrap_content = BeautifulSoup(page_content.content, "html.parser")
            job_elements = scrap_content.find_all("div", class_= "fred-categories-group")
            for job in job_elements:
                if "Money, Banking, & Finance" in job.find("strong").getText():
                    data = [{"url" : self.base_url + str(job[0].attrs.get("href")),"title": job[0].text,"unit":job[1].text} for job in list(zip(job.findAllNext("a"),job.findAllNext("span")))]
                    data = pd.DataFrame(data)
                    data["last_updated_on"] = datetime.now()
                    data.to_csv("scrap_data.csv")
        except Exception as e:
            print(f"Exception Occurred : {e}")


if __name__ == "__main__":
    FRED_Scrapper(BASEURL,ENDPOINT)