import pandas as pd
import re


class Cleaner:
    def __init__(self):
        return None

    def load_data(self, file_loc):
        data = pd.read_csv(file_loc)
        return data

    def remove_cols(self, data, cols):
        data.drop(cols, axis=1, inplace=True)
        return data

    def clean_location(self, data):
        data["location"].replace(
            {
                "Glenorcky": "Glenorchy",
                "Antwerp2": "Antwerp",
                "Multiple Locations": "Vancouver",
            },
            inplace=True,
        )
        return data

    def clean_country(self, data):
        data["country"] = data["country"].apply(lambda x: x.replace("\xa0", ""))
        data["country"] = data["country"].apply(str)
        data["country"] = data["country"].apply(lambda x: self.cleaned_text(x))
        return data

    def check_remove_duplicates(self, data):
        data.drop_duplicates(keep="first", inplace=True)
        data.reset_index(drop=True, inplace=True)
        return data

    def cleaned_text(self, text):
        text = re.sub(" ", "", text)
        text = " ".join(text.split())
        return text

    def create_meta_data(self, data):
        meta_data = pd.DataFrame()
        meta_data["aug_id"] = "aishub" + data["id"].astype(str)
        meta_data["original_id"] = data["id"]
        meta_data["sample_frequency"] = "Daily"
        meta_data["name"] = "aishub station time series data"
        meta_data[
            "description"
        ] = "List of stations from AIS HUB and their status with number of vessels online"
        meta_data["source"] = "AISHub"
        meta_data["url"] = data["url"]
        meta_data["country_name"] = data["country"]
        meta_data["location"] = data["location"]
        meta_data["time stamp"] = (
            data["timezone"] + " " + data["time"] + " " + data["date"]
        )
        return meta_data

    def save_data(self, data, filename):
        data.to_csv(filename, index=False)
        return None


if __name__ == "__main__":
    clean = Cleaner()
    ais_step1 = clean.load_data("ais_time_series_data.csv")
    ais_step2 = clean.remove_cols(ais_step1, ["Null", "contributor"])
    ais_step3 = clean.check_remove_duplicates(ais_step2)
    ais_step4 = clean.clean_location(ais_step3)
    ais_step5 = clean.clean_country(ais_step4)
    clean.save_data(ais_step5, "clean_ais_data.csv")
    meta_info = clean.create_meta_data(ais_step5)
    clean.save_data(meta_info, "ais_meta_data.csv")
    header_step1 = clean.load_data("header_ais_time_series_data.csv")
    header_step2 = clean.remove_cols(header_step1, ["extra"])
    header_step3 = clean.check_remove_duplicates(header_step2)
    clean.save_data(header_step3, "clean_header_ais_data.csv")
