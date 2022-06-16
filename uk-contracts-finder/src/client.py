import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import csv


class UK_Scrapper:
    def __init__(self,url:str):
        self.url = url
        self.scrapper.__call__()

    def scrapper(self):
        try:
            f = open("ukContracts.csv", "w")
            f.truncate()
            f.close()
            
            page_content = requests.get(self.url)
            scrap_content = BeautifulSoup(page_content.content, "html.parser")
            job_elements = scrap_content.find_all("div", class_= "search-result")
            
            colNames = ["Title",
                        "Issuer",
                        "Description",
                        "Link to tender",
                        "Procurement stage",
                        "Notice status",
                        "Closing",
                        "Contract location",
                        "Contract value",
                        "Publication date",
                        "Last Updated"
                    
                ]
            
            with open('ukContracts.csv', 'a', encoding='UTF8', newline='') as f: #create file named data.csv for output
                    writer = csv.writer(f)

                    writer.writerow(colNames)
            
    
            for job in job_elements:
                
                data = []
                
                data.append(job.find("div", class_="search-result-header").get("title"))#Title
                data.append(job.findAll("div", class_="wrap-text")[0].get_text())#Issuer
                data.append(job.findAll("div", class_="wrap-text")[1].get_text())#Description
                
                data.append(job.findAll("a")[0]["href"])#Link to tender
                
                otherData = job.findAll("div", class_="search-result-entry")
                data.append(otherData[0].get_text().replace("Procurement stage ",""))#Procurement stage
                data.append(otherData[1].get_text().replace("Notice status ",""))#Notice status
                data.append(otherData[2].get_text().replace("Closing ",""))#Closing
                data.append(otherData[3].get_text().replace("Contract location ",""))#Contract location
                data.append(otherData[4].get_text().replace("Contract value ",""))#Contract value
                data.append(otherData[5].get_text().replace("Publication date ",""))#Publication date
                data.append(datetime.now())#Last Updated
                
                
                with open('ukContracts.csv', 'a', encoding='UTF8', newline='') as f: #create file named data.csv for output
                    writer = csv.writer(f)

                    writer.writerow(data)
                
                #break
        except Exception as e:
            print(f"Exception Occurred : {e}")


if __name__ == "__main__":
    UK_Scrapper("https://www.contractsfinder.service.gov.uk/Search/Results")