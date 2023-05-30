import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def clean_data(filename):
    # Implement your data cleaning logic here
    df = pd.read_csv(filename)
    #print(df.head())
