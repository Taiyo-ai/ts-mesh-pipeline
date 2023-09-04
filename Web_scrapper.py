#First install requests_html using this command: pip install requests_html 
#Install pandas using: pip install pandas
from requests_html import HTMLSession
import pandas as pd

class NASAWebScraper:
    def __init__(self):
        self.session = HTMLSession()

    def search_nasa_earthdata(self, search_term, page_no):
        url = f"https://www.earthdata.nasa.gov/search?keys={search_term}&page={page_no}"
        response = self.session.get(url)
        return response

    def extract_search_results(self, response):
        results = []
        search_results = response.html.find('.mb-3.views-row')
        for result in search_results:
            title = result.find('.search-title', first=True).text.strip()
            summary = result.find('.field-content', first=True).text.strip()
            link = result.find('a[hreflang]', first=True).attrs['href']
            results.append({"Title": title, "Summary": summary, "Link": link})
        return results

if __name__ == "__main__":
    scraper = NASAWebScraper()
    search_term = input("Enter a search term: ")
    page_no = 0
    idx = 1
    S_No=[]
    Title=[]
    Summary=[]
    Link=[]
    while True:
        response = scraper.search_nasa_earthdata(search_term, page_no)
        search_results = scraper.extract_search_results(response)

        for x,result in enumerate(search_results, start=1):
            S_No.append(idx)
            Title.append(result['Title'])
            Summary.append(result['Summary'])
            Link.append('https://www.earthdata.nasa.gov'+result['Link'])

            idx+=1

        next_button = response.html.find('li.pager__item--next', first=True)
        if not next_button:
            break

        page_no += 1
    # Create a DataFrame
    df = pd.DataFrame(list(zip(S_No,Title, Summary, Link)),
    columns =['s_no','title', 'description', 'link'])
    
    # Store to csv file
    df.to_csv('ws.csv', sep=',', index=False,header=True)