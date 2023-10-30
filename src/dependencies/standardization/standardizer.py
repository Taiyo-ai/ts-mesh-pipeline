import os

import matplotlib.pyplot as plt
import pandas as pd


class ChartGenerator:
    def __init__(self, data):
        self.data = data
        self.save_path = os.getcwd()

    def bar_chart(self, x_col, y_col, title, xlabel, ylabel):
        plt.figure(figsize=(10, 6))
        plt.bar(self.data[x_col], self.data[y_col])
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45)
        plt.tight_layout()
        file_name = os.path.join(self.save_path,'bar_chart')

        plt.savefig(file_name, bbox_inches='tight')

    def scatter_plot(self, x_col, y_col, title, xlabel, ylabel):
        plt.figure(figsize=(10, 6))
        plt.scatter(self.data[x_col], self.data[y_col])
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        file_name = os.path.join(self.save_path,'scatter_plot')
        plt.savefig(file_name, bbox_inches='tight')

    def line_chart(self, x_col, y_col, title, xlabel, ylabel):
        plt.figure(figsize=(10, 6))
        plt.plot(self.data[x_col], self.data[y_col])
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    # Read your CSV data into a DataFrame
    data = pd.read_csv('geocoder.csv')

    # Create an instance of the ChartGenerator class
    chart_generator = ChartGenerator(data)

    # Generate a bar chart
    chart_generator.bar_chart('Region', 's_no', 'Bar Chart Example', 'Region', 'Serial Number')

    # Generate a scatter plot
    chart_generator.scatter_plot('latitude', 'longitude', 'Scatter Plot Example', 'Latitude', 'Longitude')

    # Generate a line chart
    # chart_generator.line_chart('date', 'body', 'Line Chart Example', 'Date', 'Body')
