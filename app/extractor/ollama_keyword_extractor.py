from typing import List, Dict, Any
from app.data.site_link import SiteLink
from app.data.site_keyword import SiteKeyword
from ollama import chat, ChatResponse
from app.extractor.base_collector import BaseExtractor
import json

class OllamaKeywordExtractor(BaseExtractor):

    def __init__(self, date, model, name, prompt, links: List[SiteLink], chunk):
        super().__init__("ollama", date, model, name, prompt, links, chunk)


    def call_api(self, links: List[SiteLink]) -> List[SiteKeyword] :
        response: ChatResponse = chat(
            model = self.model,
            messages=[
                {
                    'role' : 'system',
                    'content' : self.prompt
                },
                {
                    'role' : 'user',
                    'content': self.get_contents(links)
                }
            ]
        )
        return self.get_site_keywords(response.message.content)

    def run(self) -> List[SiteKeyword]:
        print(f"start ollama {self.model} {self.name}")
        links = [self.links[i:i + self.chunk] for i in range(0, len(self.links), self.chunk)]
        result_map : Dict[str, SiteKeyword] = {}
        if len(links) > 1:
            links[len(links)-2].extend(links[len(links)-1])
            del links[len(links)-1]
        for link in links:
            results = self.call_api(link)
            for result in results:
                if( result.keyword in result_map) :
                    if result_map[result.keyword].point < result.point:
                        result_map[result.keyword] = result
                else:
                    result_map[result.keyword] = result
        return [ result_map[key] for key in result_map.keys()]