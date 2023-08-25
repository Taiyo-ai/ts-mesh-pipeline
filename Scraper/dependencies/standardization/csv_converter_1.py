import csv
def csv_converter(name, data, pointer, csv_header=None,var=None):
    with open(name, 'w', newline='', encoding='utf-8') as csv_file:
        
        if pointer == 'task1':
            writer = csv.writer(csv_file)
            writer.writerow(['API Name', 'Description'])  # Write header manually
            for api_name, description in data.items():
                writer.writerow([api_name, description])
            print("Successful")
        elif pointer == 'task2':
            writer = csv.DictWriter(csv_file, fieldnames=csv_header)
            writer.writeheader()
            for row in data:
                csv_row = {key: row[key] for key in csv_header}
                writer.writerow(csv_row)
            print("Successful")
        