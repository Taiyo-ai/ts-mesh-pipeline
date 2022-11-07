# Description:
#
# The c_bls_data class uses Version 2 of the US Bureau of Labor Statistics (BLS) API
# to obtain one of more series of BLS data. It retrieves the data in
# JavaScript Object Notation (JSON) format, converts the data to CSV records,
# and writes those records to an output CSV file.
#
# The class can retrieve monthly data for one or more series for up to 20 years.
#
# To use this class, each use must provide their own BLS API Version 2
# registration key from here: https://data.bls.gov/registrationEngine/
#


# To use the c_bls_data class, create an instance with these inputs:
#
# 1. BLS API registration key.
# 2. Full path of file where program will write the output data in CSV form.
# 2. List of BLS data series IDs.
# 3. Start year of data.
# 4. End year of data.

import requests
import json
import csv

class c_bls_data:

    def __init__(self, reg_key, out_file_nm, series_id, start_year, end_year):

        # Set the file name variable and create the parameters for the API request.
        self.out_file_nm = out_file_nm
        
        headers = {'Content-type': 'application/json'}
        parameters = json.dumps({'seriesid' : series_id, 'startyear' : start_year, 'endyear' : end_year, 'calculations' : True , 'registrationkey' : reg_key})

        # Get data in JSON format and then write it to a CSV file.

        json_data = self.get_data(headers, parameters)

        self.write_data_to_csv(json_data)

    def get_data(self, headers, parameters):

        # Post the data request to the BLS API. Return the resulting JSON structure.

        post = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data = parameters, headers = headers)
        json_data = json.loads(post.text)

        return json_data

    def write_data_to_csv(self, json_data):

        # Convert the data from JSON format to CSV records. Write
        # each record to the specified output file.

        # Open the output file. Then, set up the field names for the CSV records and set up the CSV writer.
        with open(self.out_file_nm, mode = 'w', newline = '') as data_file:

            fieldnames = ['Series ID', 'Month', 'Value', 'Annual Percent Change']

            data_writer = csv.writer(data_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)

            # Write CSV file header.
            data_writer.writerow(fieldnames)

            # Write each record to the output file.
            for series in json_data['Results']['series']:
                series_id = series['seriesID']
                for item in series['data']:

                    # Get the basic data
                    year = item['year']
                    period_name = item['periodName']
                    value = item['value']

                    # Get the 12-month change
                    calculations = item['calculations']
                    pct_changes = calculations['pct_changes']
                    annual_pct_chg = pct_changes['12']

                    # Create a month field in the format of a date for 
                    # the first day of each month (for example: January 1, 2022).

                    month = period_name + ' 1, ' + year

                    #Write the CSV record to the output file.
                    data_writer.writerow([series_id, month, value, annual_pct_chg])