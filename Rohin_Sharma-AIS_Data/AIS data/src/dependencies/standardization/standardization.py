import pandas as pd
import ssl
import requests
from bs4 import BeautifulSoup
import re
import warnings


class Standardization:
    def __init__(self):
        return None

    def load_data(self, file_loc):
        data = pd.read_csv(file_loc)
        return data

    def add_domain_subdomain(data):
        data["domain"] = "marine navigation"
        data["sub_domain"] = "automated identification system stations"
        return data

    def scrap_iso_table(self, url):
        ssl._create_default_https_context = ssl._create_unverified_context
        result = requests.get(url)
        src = result.content
        soup = BeautifulSoup(src, "html.parser")
        table = soup.find("table")
        rows = table.find_all("tr")
        data = []
        for r in rows:
            td = r.find_all("td")
            rw = [r.text for r in td]
            data.append(rw)
        iso_data = pd.DataFrame(
            data,
            columns=[
                "Country name",
                "Official state name",
                "Sovereignty",
                "Alpha-2 code",
                "Alpha-3 code",
                "Numeric code",
                "Subdivision code links",
                "Internet ccTLD",
            ],
        )
        return iso_data

    def clean_text(self, text):
        text = re.sub("'", "", text)
        text = re.sub("[\(\[].*?[\)\]]", "", text)
        text = re.sub("[^a-zA-Z]", " ", text)
        text = " ".join(text.split())
        return text

    def clean_text2(self, text):
        text = re.sub("\n", "", text)
        text = " ".join(text.split())
        return text

    def cleaning_iso_data(self, iso_data):
        iso_data["Country name"] = iso_data["Country name"].apply(str)
        iso_data["Country name"] = iso_data["Country name"].apply(
            lambda x: self.clean_text(x)
        )
        iso_data["Official state name"] = iso_data["Official state name"].apply(str)
        iso_data["Official state name"] = iso_data["Official state name"].apply(
            lambda x: self.clean_text(x)
        )
        iso_data["Sovereignty"] = iso_data["Sovereignty"].apply(str)
        iso_data["Sovereignty"] = iso_data["Sovereignty"].apply(
            lambda x: self.clean_text(x)
        )
        iso_data["Alpha-2 code"] = iso_data["Alpha-2 code"].apply(str)
        iso_data["Alpha-2 code"] = iso_data["Alpha-2 code"].apply(
            lambda x: self.clean_text(x)
        )
        iso_data["Alpha-3 code"] = iso_data["Alpha-3 code"].apply(str)
        iso_data["Alpha-3 code"] = iso_data["Alpha-3 code"].apply(
            lambda x: self.clean_text(x)
        )
        iso_data["Numeric code"] = iso_data["Numeric code"].apply(str)
        iso_data["Numeric code"] = iso_data["Numeric code"].apply(
            lambda x: self.clean_text2(x)
        )
        iso_data["Subdivision code links"] = iso_data["Subdivision code links"].apply(
            str
        )
        iso_data["Subdivision code links"] = iso_data["Subdivision code links"].apply(
            lambda x: self.clean_text2(x)
        )
        iso_data["Internet ccTLD"] = iso_data["Internet ccTLD"].apply(str)
        iso_data["Internet ccTLD"] = iso_data["Internet ccTLD"].apply(
            lambda x: self.clean_text(x)
        )
        iso_data["Alpha-2 code"][2] = "AF"
        return iso_data

    def iso_code_embedded(self, url, data):
        iso_dat = self.scrap_iso_table(url)
        iso_data_clean = self.cleaning_iso_data(iso_dat)
        data["region_name"] = None
        data["country_code"] = None
        data["region_code"] = None
        for i in range(len(data)):
            for j in range(len(iso_data_clean)):
                if iso_data_clean["Country name"][j] == data["country_name"][i]:
                    data["region_name"][i] = iso_data_clean["Official state name"][j]
                    data["country_code"][i] = iso_data_clean["Alpha-3 code"][j]
                    data["region_code"][i] = iso_data_clean["Numeric code"][j]
        return data

    def save_data(self, data, filename):
        data.to_csv(filename, index=False)
        return None


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    standard = Standardization()
    data = standard.load_data("ais_meta_data_geocoded.csv")
    standard_data = standard.iso_code_embedded(
        "https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes", data
    )
    standard.save_data(standard_data, "final_ais_meta_data.csv")
