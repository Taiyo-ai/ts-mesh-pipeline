def filter(country,var,data):
    return data['data'][var][f'country/{country}'][0]['series']