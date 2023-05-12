import urllib.request
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

url = "https://www.bea.gov/news/2023/personal-income-and-outlays-march-2023"

with urllib.request.urlopen(url) as i:
    html = i.read()

data = pd.read_html(html)[0]
data.to_csv("data_march.csv", index=False)
data = pd.read_csv('data_march.csv')
df = data.apply(pd.to_numeric, errors='coerce')
df = data.dropna()
df.drop(0, inplace=True)
df.drop(1, inplace=True)
df.drop(13, inplace=True)
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
figure(figsize=(20, 10), dpi=80)
plt.stackplot(df['Unnamed: 0_level_0'], df['2022'], df['2022.1'], df['2023'], df['2023.1'], df['2023.2'], colors=['r', 'g', 'b', 'c', 'k'])

plt.xlabel("X")
plt.ylabel("Y")
plt.title("Stack Plot")
plt.legend(['JAN-2023', 'FEB-2023', 'MAR-2023', 'NOV-2022', 'DEC-2022'])
plt.show()
