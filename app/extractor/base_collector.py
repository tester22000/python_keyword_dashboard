from dataclasses import dataclass
from typing import List
from abc import ABC, abstractmethod
from app.data.site_keyword import SiteKeyword
from app.data.site_link import SiteLink
import json


class BaseExtractor(ABC):
    def __init__(self, llm, date, model, name, prompt, links: List[SiteLink], chunk):
        self.llm = llm
        self.date = date
        self.model = model
        self.name = name
        self.prompt = prompt
        self.links = links
        self.chunk = chunk

    def get_contents(self, links :List[SiteLink]) -> str :
        return '\n'.join([ link.title for link in links])


    def get_site_keywords(self, response:str ) -> List[SiteKeyword]:
        result = []
        try:
            if 'json' in response:
                start_index = response.find('[', response.find('```json'))
                end_index = response.rfind(']') + 1
                json_array = json.loads(response[start_index:end_index])
            else:
                json_array = json.loads(response)
            for json_data in json_array:
                if "keyword" in json_data and "score" in json_data:
                    result.append(SiteKeyword(
                        llm = self.llm,
                        model = self.model,
                        date = self.date,
                        name = self.name,
                        keyword = json_data['keyword'],
                        point = int(json_data['score'])
                    ))
        except Exception as e:
            print(f"response={response}")
            print(f"json decoding error {e}")

        return result

    @abstractmethod
    def run(self) -> List[SiteKeyword]:
        pass
