
import pandas as pd


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
         return data

     def check_remove_duplicates(self, data):
         data.drop_duplicates(keep="first", inplace=True)
         data.reset_index(drop=True, inplace=True)
         return data

     def save_data(self, data, filename):
         data.to_csv(filename, index=False)
         return None


 if __name__ == "__main__":
     clean = Cleaner()
     fred_step1 = clean.load_data("FRED_data.csv")
     fred_step2 = clean.remove_cols(fred_step1, ["Null", "contributor"])
     fred_step3 = clean.check_remove_duplicates(fred_step2)
     fred_step4 = clean.clean_location(fred_step3)
     fred_step5 = clean.clean_country(fred_step4)
     clean.save_data(fred_step5, "clean_fred_data.csv")
     header_step1 = clean.load_data("header_fred_data.csv")
     header_step2 = clean.remove_cols(header_step1, ["extra"])
     header_step3 = clean.check_remove_duplicates(header_step2)
     clean.save_data(header_step3, "clean_header_fred_data.csv")
