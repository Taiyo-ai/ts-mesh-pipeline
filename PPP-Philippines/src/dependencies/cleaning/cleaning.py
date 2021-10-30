import pandas as pd


class MyClass:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config")
        self.df = self.config['df']

    def clean_empty_cols(self):
        """removing columns with mostly empty entries"""
        self.df.drop('Indicative Cost', axis=1, inplace=True)
        self.df.drop('Winning Bidder/s', axis=1, inplace=True)

    def remove_duplicates(self):
        """deleting rows with duplicate data"""
        self.df.drop_duplicates(keep=False, inplace=True)

    def drop_na(self):
        """dropping rows with nan values"""
        self.df.dropna()

    def run(self):
        """putting everything together"""
        self.clean_empty_cols()
        self.remove_duplicates()
        self.drop_na()
        return self.df


if __name__ == "__main__":
    config = {'df': pd.DataFrame()}
    obj = MyClass(config=config)
    obj.run()
