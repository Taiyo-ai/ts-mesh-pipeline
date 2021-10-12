
data_content = []
for row in rows:
    cells = row.find_all('td')
    if len(cells) > 1:
        print(cells[1].get_text())
        country_link = cells[1].find('a')
        country_info = [cell.text.strip('\n') for cell in cells]
        additional_details = getAdditionalDetails(country_link.get('href'))
        if (len(additional_details) == 4):
            country_info += additional_details
            data_content.append(country_info)

dataset = pd.DataFrame(data_content)

# Define column headings
headers = rows[0].find_all('th')
headers = [header.get_text().strip('\n') for header in headers]
headers += ['Total Area', 'Percentage Water', 'Total Nominal GDP', 'Per Capita GDP']
dataset.columns = headers

drop_columns = ['Rank', 'Date', 'Source']
dataset.drop(drop_columns, axis = 1, inplace = True)
dataset.sample(3)

dataset.to_csv("Dataset.csv", index = False)
