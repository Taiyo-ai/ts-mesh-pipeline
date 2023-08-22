import requests
from xml.etree import ElementTree as ET

class BEARestAPIScraper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://apps.bea.gov/api/data/"

    def fetch_data(self, method, dataset=None, parameter=None):
        params = {
            "USERID": self.api_key,
            "METHOD": method,
            "RESULTFORMAT": "XML"
        }
        if dataset:
            params["DATASETNAME"] = dataset
        if parameter:
            params["PARAMETERNAME"] = parameter
        
        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Failed to fetch data from BEA API. Status code: {response.status_code}")

if __name__ == "__main__":
    api_key = "7142D42F-31AF-4831-A5E6-24765CA74CD4"
    scraper = BEARestAPIScraper(api_key)

    # Get Parameter List for the GDPbyIndustry dataset
    dataset_name = "IIP"
    method = "GetParameterList"
    data = scraper.fetch_data(method=method, dataset=dataset_name)

    # Parse XML response
    root = ET.fromstring(data)
    error_element = root.find(".//Error")
    if error_element is not None:
        api_error_code = error_element.get("APIErrorCode")
        api_error_desc = error_element.get("APIErrorDescription")
        print(f"API Error: Code {api_error_code}, Description: {api_error_desc}")
    else:
        # Process and use the XML data as needed
        parameters = root.findall(".//Parameter")
        for parameter in parameters:
            param_name = parameter.get("ParameterName")
            param_desc = parameter.get("ParameterDescription")
            print(f"Parameter Name: {param_name}, Description: {param_desc}")
