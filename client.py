from scraper import DCHarvester
from concurrent.futures import ThreadPoolExecutor


def get_data(country_code,country_name,stat_var,):
    df = DCHarvester(country_code,stat_var).get_series()
    df['Country Name'] = [country_name for i in range(len(df))]
    df.to_csv(f'{country_code}_{stat_var}.csv')

if __name__ == '__main__':
    stat_var = 'Count_Person_Male'
    countries = [['USA','USA'], ['KR','South Korea'],['IND','India'],['JPN','Japan']]
    scrape = lambda x: get_data(x[0],x[1],stat_var=stat_var)

    with ThreadPoolExecutor() as exe:
        exe.map(scrape,countries)
