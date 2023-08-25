import csv


# Write the data to a CSV file
def ctt(csv_filename,data,var):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
       csv_writer = csv.writer(csvfile)
    
    # Write the header
       csv_writer.writerow(['Title','date', 'value'])
    
    # Write the data rows
       for i in data:
         csv_writer.writerow([var,i['date'],i['value']])
        