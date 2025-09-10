import requests
from dataclasses import dataclass
from typing import List
from abc import ABC, abstractmethod
import re


@dataclass
class LinkTitle:
    name: str
    link: str
    title: str

    def __hash__(self):
        return hash(self.link) 

class BaseCollector(ABC):
    def __init__(self, name, base_url):
        self.name = name
        self.base_url = base_url
    
    def getLinkTitle(self, hrefObj) -> LinkTitle:
        #href = re.sub(r'\?.*','',requests.compat.urljoin(self.base_url, hrefObj.get('href')))
        href = requests.compat.urljoin(self.base_url, hrefObj.get('href'))
        #a.replace('\n','').replace('"','').replace('“','').replace('”','')
        title= re.sub(r"[\n'\"\“\”\‘\’]", " ", hrefObj.text).strip()
        if len(title)>100 :
            title = title[0:100]
        return LinkTitle(self.name, href, title)

    def is_target(self, href:str, keyword:str, exclude:str) -> bool :
        if len(exclude) >0 and len([ data for data in exclude if data in href]) > 0:
            return False
        if keyword in href:
            return True
        return False

    def is_not_exclude(self, href:str, exclude:str) -> bool :
        if len(exclude) >0 and len([ data for data in exclude if data in href]) > 0:
            return False
        return True

    @abstractmethod
    def run(self) -> List[LinkTitle]:
        pass