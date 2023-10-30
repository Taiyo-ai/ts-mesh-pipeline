import datetime
import pandas as pd

class Cleaner():

    def __init__(self):

        # Use The Path of Raw Data
        self.df = pd.read_csv(r'C:\Users\ox\PycharmProjects\Prism_v01\Taiyo\Sats_Kanna\taiyo.csv')

    def clean_date(self, value):
        date_obj = datetime.datetime.strptime(value, '%m-%d-%Y')
        date = datetime.datetime.strftime(date_obj, '%Y-%m-%d')
        return date

    def cleaner(self):
        print('Cleaner Triggered')
        self.df['date'] = self.df['time'].apply(lambda d: self.clean_date(d))
        self.df.drop(columns=['time'], inplace=True)
        # Execute The Required Cleaner Function Here

        self.df.to_csv('cleaner.csv', index=False)
