import pandas as pd
from selenium import webdriver

class TenderScraper:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = self.setup_driver()

    def setup_driver(self):
        service = webdriver.ChromeService(executable_path=self.driver_path)
        return webdriver.Chrome(service=service)

    def scrape_tender_details(self, url):
        self.driver.get(url)

        tenders_headings = []
        head = self.driver.find_elements(by='xpath', value="//h1[@class='fl w645']")
        for i in head:
            heading_text_1 = i.text
            tenders_headings.append(heading_text_1)

        details = []
        d = self.driver.find_elements(by='xpath', value='//div[@class="property mt10"]')
        for i in d:
            details_list = i.text
            details.append(details_list)

        def split_list_items(details):
            industry_list, region_list, source_list = [], [], []
            for item in details:
                parts = item.split('Region:')
                industry = parts[0].split(':')[1]
                region = parts[1].split('source:')[0]
                source = parts[1].split('source:')[1]

                industry_list.append(industry)
                region_list.append(region)
                source_list.append(source)

            return industry_list, region_list, source_list

        industry, region, source = split_list_items(details)

        df_details = pd.DataFrame({
            'Tender_Headings': tenders_headings,
            'Industry': industry,
            'Region': region,
            'Source': source
        })

        return df_details

    def close_driver(self):
        self.driver.quit()


if __name__ == "__main__":
    driver_path = r'C:\Users\anura\Desktop\Web Scrapping\chromedriver-win64\chromedriver.exe'
    url = 'http://en.chinabidding.mofcom.gov.cn/channel/EnSearchList.shtml?provinceCodeShow=&capitalSourceCodeShow=&keyword=tenders&tenders=1&industry='

    scraper = TenderScraper(driver_path)
    result_df = scraper.scrape_tender_details(url)
    print(result_df)

    # Close the driver
    scraper.close_driver()
