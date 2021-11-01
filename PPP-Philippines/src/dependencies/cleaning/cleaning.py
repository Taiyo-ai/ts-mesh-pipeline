import pandas as pd
import re


class MyClass:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config")
        self.df = self.config['df']

    def strip_special(self):
        for index, row in self.df.iterrows():
            if re.sub('[^A-Za-z0-9]+', '', row['project_description']) == '':
                row['project_description'] = ''
            try:
                temp = re.sub(r'[a-z,]', '', row['project_cost'].lower())
                self.df['project_cost'][index] = float(temp)
            except AttributeError:
                self.df['project_cost'][index] = float('Nan')
            try:
                temp = re.sub(r'[a-z,]', '', row['indicative_cost'].lower())
                self.df['indicative_cost'][index] = float(temp)
            except AttributeError:
                self.df['indicative_cost'][index] = float('Nan')
        self.df.rename({'project_cost': 'project_cost(in_million_php)'},
                       axis=1, inplace=True)
        self.df.rename({'indicative_cost': 'indicative_cost(in_million_php)'},
                       axis=1, inplace=True)

    def remove_col(self, col_name):
        """function to remove columns with mostly empty entries"""
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

    def replace_nan(self, replace_str, col_name='all'):
        """function to replace nan values with given replace_str.
        If col_name is given, NaN values in the corresponding column are
        replaced with replace_str.
        By default all NaN values are replaced."""
        nan_value = float("NaN")
        self.df.replace(to_replace='', value=replace_str, inplace=True)
        if col_name == 'all':
            self.df.replace(to_replace=nan_value, value=replace_str,
                            inplace=True)
        else:
            self.df[self.df[col_name].isnull()] = replace_str

    def run(self):
        """using cleaning functions as per use case"""
        self.remove_duplicates()
        self.strip_special()
        self.replace_nan('TBD')
        return self.df


if __name__ == "__main__":
    config = {'df': pd.DataFrame()}
    obj = MyClass(config=config)
    obj.run()
