import csv
import xml.etree.ElementTree as ET
import xml.dom.minidom
from client import BEAScraper

def save_to_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def main():
    api_key = "7142D42F-31AF-4831-A5E6-24765CA74CD4"
    client = BEAScraper(api_key)

    # Example: Get Dataset List
    dataset_list_result = client.fetch_data("GetDataSetList")
    dataset_list = client.process_response(dataset_list_result)["data"]

    # Parse XML data for datasets
    datasets = []
    root = ET.fromstring(dataset_list)
    for dataset in root.findall("Results/Dataset"):
        dataset_name = dataset.get("DatasetName")
        dataset_desc = dataset.get("DatasetDescription")
        datasets.append([dataset_name, dataset_desc])

    # Save datasets to CSV
    save_to_csv(datasets, "datasets.csv")
    print("Datasets saved to datasets.csv")

    # Example: Get Parameter List for a chosen dataset
    chosen_dataset = "GDPbyIndustry"  # Choose a valid dataset from the dataset_list
    parameter_list_result = client.get_parameter_list(chosen_dataset)
    parameter_list = parameter_list_result["data"]

    # Parse XML data for parameters
    parameters = []
    root = ET.fromstring(parameter_list)
    for parameter in root.findall("Results/Parameter"):
        param_name = parameter.get("ParameterName")
        param_desc = parameter.get("ParameterDescription")
        parameters.append([param_name, param_desc])

    # Save parameters to CSV
    save_to_csv(parameters, "parameters.csv")
    print("Parameters saved to parameters.csv")

    # Example: Get Parameter Values for a chosen dataset and parameter
    chosen_parameter = "Industry"  # Choose a valid parameter from the parameter_list
    parameter_values_result = client.get_parameter_values(chosen_dataset, chosen_parameter)
    parameter_values = parameter_values_result["data"]

    # Parse XML data for parameter values
    param_values = []
    root = ET.fromstring(parameter_values)
    for param_value in root.findall("Results/ParamValue"):
        key = param_value.get("Key")
        desc = param_value.get("Desc")
        param_values.append([key, desc])

    # Save parameter values to CSV
    save_to_csv(param_values, "parameter_values.csv")
    print("Parameter values saved to parameter_values.csv")

if __name__ == "__main__":
    main()
