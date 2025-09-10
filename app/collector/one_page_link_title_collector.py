import requests
from bs4 import BeautifulSoup
import time
from typing import List
from app.collector import LinkTitle, BaseCollector

class OenPageLinkTitleCollector(BaseCollector):

    def __init__(self, name, url, keyword, exclude):
        self.keyword = keyword
        if len(exclude.strip()) > 0:
            self.excludes = exclude.strip().split(',')
        else:
            self.excludes = []
        super().__init__(name, url)

    def run(self) -> List[LinkTitle]:
        lists = []
        
        try:
            response = requests.get(self.base_url, timeout=10)
            response.raise_for_status() # HTTP 오류 발생 시 예외 처리

            soup = BeautifulSoup(response.text, 'html.parser')
            
            article_links = soup.select('a')

            for link in article_links:
                href = link.get('href')
                if self.is_target(href, self.keyword, self.excludes):
                    lists.append(self.getLinkTitle(link))


        except requests.exceptions.RequestException as e:
            print(f"Error collecting URLs from {self.base_url}: {e}")

        return list(set(lists))