import pandas as pd
import re


class MyClass:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config")
        self.df = self.config['df']

    def strip_special(self):
        for index, row in self.df.iterrows():
            if re.sub('[^A-Za-z0-9]+', '', row['Project Description']) == '':
                row['Project Description'] = ''
            try:
                temp = re.sub(r'[a-z,]', '', row['Project Cost'].lower())
                print(temp)
                self.df['Project Cost'][index] = temp
            except AttributeError:
                pass
        self.df.rename({'Project Cost': 'Project Cost(in million Php)'},
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
