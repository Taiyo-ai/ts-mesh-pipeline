import pandas as pd
import re


class DataCleaner:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config")
        self.df = self.config['df']

    def remove_unwanted_char(self):
        """removing unwanted characters like units or unneccessary special
        characters.
        Also, renaming columns with units."""
        for index, row in self.df.iterrows():
            if re.sub('[^A-Za-z0-9]+', '', row['project_description']) == '':
                row['project_description'] = ''
            try:
                temp = re.sub(r'[a-z,]', '', row['project_cost'].lower())
                if temp == '':
                    self.df['project_cost'][index] = float("Nan")
                else:
                    self.df['project_cost'][index] = temp
            except AttributeError:
                pass
            try:
                temp = re.sub(r'[a-z,]', '', row['indicative_cost'].lower())
                if temp == '':
                    self.df['indicative_cost'][index] = float("Nan")
                else:
                    self.df['indicative_cost'][index] = temp
            except AttributeError:
                pass
        self.df.rename({'project_cost': 'project_cost(in_million_php)'},
                       axis=1, inplace=True)
        self.df.rename({'indicative_cost': 'indicative_cost(in_million_php)'},
                       axis=1, inplace=True)

    def change_col_type(self):
        """function to change data types of columns"""
        for col in self.df.columns:
            if col == 'project_cost(in_million_php)':
                self.df[col] = pd.to_numeric(self.df[col])
            elif col == 'indicative_cost(in_million_php)':
                self.df[col] = self.df[col].astype(float)
            else:
                self.df[col] = self.df[col].astype(str)

    def remove_col(self, col_name):
        """function to remove columns"""
        self.df.drop(col_name, axis=1, inplace=True)

    def remove_duplicates(self):
        """function to delete rows with duplicate data"""
        self.df.drop_duplicates(keep=False, inplace=True)

    def drop_nan(self, col_name='all'):
        """function to drop rows with nan values.
        If col_name is given, rows is NaN values in the corresponding
        column are removed."""
        if col_name == 'all':
            for col in self.df.columns:
                self.df.dropna(subset=[col], inplace=True)
            self.df.dropna(inplace=True)
        else:
            self.df.dropna(subset=[col_name], inplace=True)

    def replace_nan(self):
        """function to replace nan values with given replace_str.
        If col_name is given, NaN values in the corresponding column are
        replaced with replace_str.
        By default all NaN values are replaced."""
        for col in self.df.columns:
            if col not in ['project_cost(in_million_php)',
                           'indicative_cost(in_million_php)']:
                self.df[col].replace('', 'TBD', inplace=True)

    def run(self):
        """using cleaning functions as per use case"""
        self.remove_duplicates()
        self.remove_unwanted_char()
        self.replace_nan()
        self.change_col_type()
        return self.df


if __name__ == "__main__":
    config = {'df': pd.DataFrame()}
    obj = DataCleaner(config=config)
    obj.run()
