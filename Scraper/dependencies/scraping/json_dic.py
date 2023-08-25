def json_dic(url,params,headers):
    import requests
    response = requests.get(url,params = params,headers= headers)
    if response.status_code ==200:
        data = response.json(object_hook =((dict['URL','0'])))
        modified_data = [{key: value for key, value in entry.items() if key not in ('0', '3','2','1')} for entry in data]
        return modified_data
    return response