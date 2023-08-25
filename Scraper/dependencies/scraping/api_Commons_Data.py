def api_Commons_Data(country_entities,variable):
    import requests

    cookies = {
            '_ga': 'GA1.1.71160719.1692872310',
            '_ga_KWSES5WXZE': 'GS1.1.1692946096.3.1.1692950172.0.0.0',
            }

    headers = {
            'authority': 'www.datacommons.org',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
    # 'cookie': '_ga=GA1.1.71160719.1692872310; _ga_KWSES5WXZE=GS1.1.1692946096.3.1.1692950172.0.0.0',
            'origin': 'https://www.datacommons.org',
            'referer': 'https://www.datacommons.org/tools/timeline',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.54',
            }

# json_data = {
#     'dcid': 'dc/g/Root',
#     'entities': [
#         'country/DEU',
#     ],
# }
    # params = {
    #         'entities': 'country/DEU',
    #           'variables': 'FertilityRate_Person_Female',
    #         }
    params = {
        'entities': f'country/{country_entities}',
        'variables': f'{variable}',
    }
    
    
    response = requests.get(
        'https://www.datacommons.org/api/observations/series/all',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    
    # response = requests.post('https://www.datacommons.org/api/variable-group/info', cookies=cookies, headers=headers, json=json_data)
    return response.json()






        
        # Write the header
        
        