# dear sir , the assignment details ,links you gave me was not very understandable to me as i've just learnt data scrapping in this week . i was really tough for me to get and extract the data
# therefore i tried to do simpe data scrapping from property websites.
from bs4 import BeautifulSoup
import requests
from csv import writer
r=requests.get("https://www.99acres.com/search/property/buy/mumbai?city=12&keyword=mumbai&preference=S&area_unit=1&res_com=R")
#print(r)
soup=BeautifulSoup(r.content,'html.parser')
lists=soup.find_all('div',class_="srpTuple__tupleDetails")
with open('housing.csv','w',encoding='utf8',newline='')as f:
    thewriter=writer(f)
    header=['Title','Price per sq feet','Area','Price','Location']
    thewriter.writerow(header)
    for list in lists:
        title=list.find('a',class_="srpTuple__dFlex")
    
        pricepersqfeet=list.find('div',class_="srp_tuple_price_per_unit_area")
        area=list.find('td',class_="srp_tuple_primary_area")
        price=list.find('td',class_="srp_tuple_price")
        location=list.find('a',class_="body_med srpTuple__propertyName").text
        info=[title,pricepersqfeet,area,price,location]
        thewriter.writerow(info)




