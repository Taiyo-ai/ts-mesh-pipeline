from io import FileIO
import requests 
import os

def dataScrapper()->FileIO:
    """Scrapper function to scrap the station data"""
    url= 'https://www.aishub.net/stations/export'
    
    #Establishing connection ...
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Failed! to establish the connection")
   
    #Getting the text document
    text =  response.text

    #Saving into csv file 
    with open("../../data/ScrappedData.csv", 'w') as file:

      #Splitting with raw and newline
      lns = text.split("\r\n")
      for item in lns:
        file.write(item.replace("=", ",") + os.linesep)
    

