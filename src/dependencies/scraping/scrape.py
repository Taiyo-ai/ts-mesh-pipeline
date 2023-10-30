from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
import json
import logging

class Scraper():

    def __init__(self):
        self.dict_ = []
        self.main_link = 'http://en.chinabidding.mofcom.gov.cn/zbwcms/front/en/bidding/bulletinList'
        self.header = {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,bn;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '83',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'insert_cookie=67183482',
            'Host': 'en.chinabidding.mofcom.gov.cn',
            'Origin': 'http://en.chinabidding.mofcom.gov.cn',
            'Referer': 'http://en.chinabidding.mofcom.gov.cn/channel/EnSearchList.shtml?tenders=1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }


    @staticmethod
    def get_dictionary(s_no=None, title=None, body=None, industry=None, region=None, source=None, time=None):
        dictionary = {
            's_no': s_no,
            'title': title,
            'body': body,
            'industry': industry,
            'region': region,
            'source': source,
            'time': time,
        }
        return dictionary

    def scrape_data(self):
        print('Scraper Triggered')
        page_payload = {
            'pageNumber': 1,
            'pageSize': '10',
            'type': '1',
            'industry': '',
            'provinceCode': '',
            'keyword': '',
            'capitalSourceCode': '',
        }
        page_req = requests.post(self.main_link, data=page_payload)
        page_data = json.loads(page_req.text)
        # page_count = page_data['maxPageNum']
        '''page count for sample data'''
        page_count = 10
        print(f'{page_count} Pages To Scrape')
        for i in range(1, page_count):
            payload = {
            'pageNumber': f'{i}',
            'pageSize': '100',
            'type': '1',
            'industry': '',
            'provinceCode': '',
            'keyword': '',
            'capitalSourceCode': '',
            }
            r = requests.post(self.main_link, data=payload)
            data = json.loads(r.text)
            rows = data['rows']

            for rows_ in rows:
                industry = rows_['industryName']
                region = rows_['areaName']
                source = rows_['capitalSourceName']
                title = rows_['name']
                body = rows_['digest']
                time = rows_['publishTime']

                dictionary = self.get_dictionary(s_no=1, title=title, body=body, industry=industry, region=region, source=source, time=time)
                self.dict_.append(dictionary)
        df = pd.DataFrame(self.dict_)
        df.to_csv(f'taiyo.csv', index=False)

