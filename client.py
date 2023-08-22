import requests
from xml.etree import ElementTree as ET

class BEAScraper:
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

    def process_response(self, data):
        root = ET.fromstring(data)
        error_element = root.find(".//Error")
        if error_element is not None:
            api_error_code = error_element.get("APIErrorCode")
            api_error_desc = error_element.get("APIErrorDescription")
            return {"error": f"API Error: Code {api_error_code}, Description: {api_error_desc}"}
        else:
            # Process and extract data as needed
            return {"data": ET.tostring(root, encoding='utf-8').decode('utf-8')}

    def get_parameter_list(self, dataset):
        parameter_list_result = self.fetch_data("GetParameterList", dataset)
        return self.process_response(parameter_list_result)

    def get_parameter_values(self, dataset, parameter):
        parameter_values_result = self.fetch_data("GetParameterValues", dataset, parameter)
        return self.process_response(parameter_values_result)
