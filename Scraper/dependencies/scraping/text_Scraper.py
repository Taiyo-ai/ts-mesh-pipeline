def text_Scraper(url,tags ,class_=None):
    
    import requests
    data= []
    from bs4 import BeautifulSoup
    respond = requests.get(url)
    if respond.status_code == 200:
        soup = BeautifulSoup(respond.content,'html.parser')
        element = soup.find_all(tags,class_)
        for i in element:
           data.append((i.text))
           return data
    return None 