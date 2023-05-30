import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import time
from wordcloud import WordCloud
def viz_data():
    # Implement your geocoding logic here
    warnings.filterwarnings("ignore")
    Org_data = pd.read_excel('IEG_ICRR-PPAR_Ratings_Q4FY22.xlsx')
    Org_data
    df = Org_data
    # Assuming you have the project data in a DataFrame named 'project_data'
    # Select the relevant columns for the plot
    data_for_plot = df[['Closing FY', 'IEG Outcome Ratings']]

    # Filter the data for the desired years
    desired_years = [2018, 2019, 2020, 2021, 2022]
    filtered_data = data_for_plot[data_for_plot['Closing FY'].isin(desired_years)]

    # Calculate the percentage distribution of ratings by project closing fiscal year
    rating_distribution = (
     filtered_data.groupby(['Closing FY', 'IEG Outcome Ratings'])
    .size()
    .groupby(level=0)
    .apply(lambda x: 100 * x / float(x.sum()))
    .reset_index(name='Percentage')
    )

    # Plot the distribution
    plt.figure(figsize=(20, 10))
    sns.barplot(x='Closing FY', y='Percentage', hue='IEG Outcome Ratings', data=rating_distribution)
    plt.title('Percentage Distribution of Ratings by Project Closing Fiscal Year (2018-2022)')
    plt.xlabel('Project Closing Fiscal Year')
    plt.ylabel('Percentage(%)')
    plt.xticks(rotation=45)
    plt.savefig('src\Images\IEG_Outcome_Ratings.png')
    # plt.show(block=False)
    # time.sleep(3)
    # plt.close()


        # Assuming you have the project data in a DataFrame named 'project_data'
    # Select the relevant columns for the plot
    data_for_plot = df[['Closing FY', 'IEG Bank Performance Ratings']]

    # Filter the data for the desired years
    desired_years = [2018, 2019, 2020, 2021, 2022]
    filtered_data = data_for_plot[data_for_plot['Closing FY'].isin(desired_years)]

    # Calculate the percentage distribution of ratings by project closing fiscal year
    rating_distribution = (
        filtered_data.groupby(['Closing FY', 'IEG Bank Performance Ratings'])
        .size()
        .groupby(level=0)
        .apply(lambda x: 100 * x / float(x.sum()))
        .reset_index(name='Percentage')
    )

    # Plot the distribution
    plt.figure(figsize=(25, 10))
    sns.barplot(x='Closing FY', y='Percentage', hue='IEG Bank Performance Ratings', data=rating_distribution)
    plt.title('Percentage Distribution of Performance Ratings by Project Closing Fiscal Year (2018-2022)')
    plt.xlabel('Project Closing Fiscal Year')
    plt.ylabel('Percentage(%)')
    plt.xticks(rotation=45)
    # Save the plot as an image
    plt.savefig('src\Images\IEG_Bank_Performance_Ratings.png')
    #plt.show(block=True)
    #time.sleep(3)
    #plt.close()


    # Assuming you have the project data in a DataFrame named 'project_data'
    # Select the relevant columns for the plot
    data_for_plot = df[['Closing FY', 'IEG Quality at Entry Ratings']]

    # Filter the data for the desired years
    desired_years = [2018, 2019, 2020, 2021, 2022]
    filtered_data = data_for_plot[data_for_plot['Closing FY'].isin(desired_years)]

    # Calculate the percentage distribution of ratings by project closing fiscal year
    rating_distribution = (
        filtered_data.groupby(['Closing FY', 'IEG Quality at Entry Ratings'])
        .size()
        .groupby(level=0)
        .apply(lambda x: 100 * x / float(x.sum()))
        .reset_index(name='Percentage')
    )

    # Plot the distribution
    plt.figure(figsize=(20, 10))
    sns.barplot(x='Closing FY', y='Percentage', hue='IEG Quality at Entry Ratings', data=rating_distribution)
    plt.title('Percentage Distribution of Quality at Entry Ratings by Project Closing Fiscal Year (2018-2022)')
    plt.xlabel('Project Closing Fiscal Year')
    plt.ylabel('Percentage(%)')
    plt.xticks(rotation=45)
    # Save the plot as an image
    plt.savefig('src\Images\IEG_Quality_at_Entry_Ratings.png')
    # plt.show(block=False)
    # time.sleep(3)
    # plt.close()

    Country = df.Country.str.cat(sep=';')
    def word_count(str):
        counts = dict()
        words = str.split(';')

        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1

        return counts

    wordCount_country = word_count(Country)
    # Generate the word cloud
    wordcloud = WordCloud(background_color='white').generate_from_frequencies(wordCount_country)

    # Create the plot
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Countries')

    # Display the plot
    plt.savefig('src\Images\Countries Distribution.png')
    # plt.show(block=False)
    # time.sleep(3)
    # plt.close()

    Region = df.Region.str.cat(sep=';')
    def word_count(str):
        counts = dict()
        words = str.split(';')

        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1

        return counts

    wordCount_region = word_count(Region)

    # Sort the dictionary by values in descending order
    sorted_counts = sorted(wordCount_region.items(), key=lambda x: x[1], reverse=True)

    # Print the sorted dictionary side by side
    # for item in sorted_counts:
    #     print("{} : {}".format(item[0], item[1]), end=" ; ")

    # Generate the word cloud
    wordcloud = WordCloud(background_color='black').generate_from_frequencies(wordCount_region)

    # Create the plot
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Region')

    # Display the plot
    plt.savefig('src\Images\Region Distribution.png')
    # plt.show(block=False)
    # time.sleep(3)
    # plt.close()

    # Assuming you have the project data in a DataFrame named 'df'
    # Group the data by project volume and count the occurrences of project IDs
    data_for_plot = df.groupby('Project Volume')['Project ID'].count()

    # Plot the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(data_for_plot, labels=data_for_plot.index, autopct='%1.1f%%', startangle=90)
    plt.title('Project Volume Distribution')
    plt.axis('equal')
    plt.savefig('src\Images\Project Volume Distribution.png')
    # plt.show(block=False)
    # time.sleep(3)
    # plt.close()

    # Assuming you have the project data in a DataFrame named 'df'
    # Group the data by project volume and count the occurrences of project IDs
    data_for_plot = df.groupby('Global Practice')['Project ID'].count()
    # Plot the pie chart
    plt.figure(figsize=(10, 10))
    plt.pie(data_for_plot, labels=data_for_plot.index, autopct='%1.1f%%', startangle=90)
    plt.title('Global Practice Distribution')
    print()
    plt.axis('equal')
    plt.savefig('src\Images\Global Practice Distribution.png')
    # plt.show(block=False)
    # time.sleep(3)
    # plt.close()
    print('Visualization Completed')
    print('Please check the Visalisation Images in the  Image folder')