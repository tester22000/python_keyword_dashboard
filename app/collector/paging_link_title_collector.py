import requests
from bs4 import BeautifulSoup
import time
from typing import List
from app.collector import LinkTitle, BaseCollector

class PagingLinkTitleCollector(BaseCollector):

    def __init__(self, name, url, page_template, page_count, a_selector, rate_limit, exclude):
        self.page_template = page_template
        self.page_count = page_count
        self.a_selector = a_selector
        self.rate_limit = rate_limit
        if len(exclude.strip()) > 0:
            self.excludes = exclude.strip().split(',')
        else:
            self.excludes = []
        super().__init__(name, url)

    def run(self) -> List[LinkTitle]:
        
        lists = []
        
        for page_num in range(1, self.page_count + 1):
            try:
                page_info = self.page_template.format(page = page_num)
                page_url = f"{self.base_url}{page_info}"
                
                self._apply_rate_limit()

                response = requests.get(page_url, timeout=10)
                response.raise_for_status() # HTTP 오류 발생 시 예외 처리

                soup = BeautifulSoup(response.text, 'html.parser')
                
                article_links = soup.select(self.a_selector) # span.titleline>a
                for link in article_links:
                    if self.is_not_exclude(link.get('href'), self.excludes):
                        lists.append(self.getLinkTitle(link))
                
            except requests.exceptions.RequestException as e:
                print(f"Error collecting URLs from {page_url}: {e}")
                continue

        return list(set(lists))
        
    def _apply_rate_limit(self):
        if self.rate_limit > 0:
            time.sleep(1 / self.rate_limit)