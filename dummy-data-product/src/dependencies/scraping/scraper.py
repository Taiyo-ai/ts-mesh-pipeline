 import datetime
 import pandas as pd
 import ssl
 import bs4 as bs
 import urllib.request
 import time


 class Scrapper:
     def __init__(self):
         return None

     def scrap_file(self, url, start_page, end_page):
         data = []
         ssl._create_default_https_context = ssl._create_unverified_context
         timezone = (
             datetime.datetime.now()
             .astimezone()
             .tzinfo.tzname(datetime.datetime.now().astimezone())
         )
         for i in range(start_page, end_page):
             today = datetime.datetime.now()
             current_time = today.strftime("%H:%M:%S")
             date_now = datetime.date.today()
             date_info = date_now.strftime("%d/%m/%Y")
             source = urllib.request.urlopen(url + "?page=" + "i").read()
             soup = bs.BeautifulSoup(source, "lxml")
             table = soup.find("table")
             table_rows = table.find_all("tr")
             table_rows.remove(table_rows[0])
             table_rows.remove(table_rows[0])
             row = []
             for tr in table_rows:
                 td = tr.find_all("td")
                 row = [i.text for i in td]
                 row.append(td[1].i.attrs["title"])
                 row.append(timezone)
                 row.append(date_info)
                 row.append(current_time)
                 data.append(row)
         return data

     def scrap_header(self, url):
         ssl._create_default_https_context = ssl._create_unverified_context
         timezone = (
             datetime.datetime.now()
             .astimezone()
             .tzinfo.tzname(datetime.datetime.now().astimezone())
         )
         today = datetime.datetime.now()
         current_time = today.strftime("%H:%M:%S")
         date_now = datetime.date.today()
         date_info = date_now.strftime("%d/%m/%Y")
         source = urllib.request.urlopen(url).read()
         soup = bs.BeautifulSoup(source, "lxml")
         data = soup.find_all("h3")
         data.remove(data[0])
         req_data = []
         req_data.append(timezone)
         req_data.append(date_info)
         req_data.append(current_time)
         req_data.extend([i.text for i in data])
         return req_data

     def time_series_limit(self, url, start_page, end_page, time_interval, time_limit):
         count = 0
         time_series_data = []
         while count < time_limit:
             count = count + 1
             start_func = time.time()
             req_data = self.scrap_file(url, start_page, end_page)
             stop_func = time.time()
             time_series_data.extend(req_data)
             time_taken = stop_func - start_func
             time.sleep(time_interval - time_taken)
         return time_series_data

     def h_time_series_limit(self, url, time_interval, time_limit):
         count = 0
         time_series_data = []
         while count < time_limit:
             count = count + 1
             start_func = time.time()
             req_data = self.scrap_header(url)
             stop_func = time.time()
             time_series_data.append(req_data)
             time_taken = stop_func - start_func
             time.sleep(time_interval - time_taken)
         return time_series_data

     def create_save_csv(self, ts_data):
         ais_data = pd.DataFrame(
             ts_data,
             columns=[
                 "id",
                 "Null",
                 "uptime",
                 "country",
                 "location",
                 "ships",
                 "distinct",
                 "contributor",
                 "status",
                 "timezone",
                 "time",
                 "date",
             ],
         )
         ais_data.to_csv("ais_time_series_data.csv", index=False)
         return None

     def save_csv(self, header_ts_data):
         header_ais_data = pd.DataFrame(
             header_ts_data,
             columns=[
                 "timezone",
                 "date",
                 "time",
                 "vessels_online",
                 "stations_online",
                 "stations_offline",
                 "extra",
             ],
         )
         header_ais_data.to_csv("header_ais_time_series_data.csv", index=False)
         return header_ais_data


 if __name__ == "__main__":
     scrap_data = Scrapper()
     ais_data = scrap_data.time_series_limit(
         "https://fred.stlouisfed.org/categories/22", 1, 9, 60.0, 30
     )
     header_data = scrap_data.h_time_series_limit(
         "https://fred.stlouisfed.org/categories/22", 10.0, 60
     )
     scrap_data.create_save_csv(fred_data)
     scrap_data.save_csv(header_data)
