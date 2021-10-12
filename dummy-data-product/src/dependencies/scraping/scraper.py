import requests
import os

from requests.api import request


class Scraping:
    def __init__(self, search_term, per_page):
        self.search_term = search_term
        self.per_page = per_page
        self.page = 0
        self.quality = quality
        self.headers = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-IN,en-US;q=0.9,en;q=0.8",
            "referer": "https://fred.stlouisfed.org/series/TERMCBPER24NS",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
        }

    def set_url(self):
        return f"https://fred.stlouisfed.org/graph/api/series/?id=TERMCBPER24NS&width=318"

    def make_request(self):
        url = self.set_url()
        return requests.request("GET", url, headers=self.headers)

    def get_data(self):
        self.data = make_request().json()

    def save_path(self, name):
        download_dir = "FRED_data"
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)
        return f"{os.path.join(os.path.replace(os.getcwd()),download_dir,name)}.csv"

    def download(self, url, name):
        filepath = self.save_path(name)
        with open(filepath, "wb") as f:
            f.write(requests.request("GET", url, headers=self.headers).content)

    def Scrapper(self, pages):
        for page in range(0, pages+1):
            self.make_request()
            self.get_data()
            for item in self.data['results']:
                name = item['id']
                url = item['urls'][self.quality]
                self.download(url, name)
            self.pages += 1


if __name__ == "__main__":
    scrapper = Scraping("TERMCBPER24NS",10)
    scrapper.Scrapper(1)
