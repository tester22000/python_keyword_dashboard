from typing import List, Dict, Any
from app.data.site_link import SiteLink
from app.data.site_keyword import SiteKeyword
import google.generativeai as genai
from app.extractor.base_collector import BaseExtractor
import os
import json

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class GeminiKeywordExtractor(BaseExtractor):
    def __init__(self, date, model, name, prompt, links: List[SiteLink], chunk):
        super().__init__("gemini", date, model, name, prompt, links, chunk)

    def call_api(self, links: List[SiteLink]) -> List[SiteKeyword] :
        try:
            model = genai.GenerativeModel(
                model_name=self.model,
                system_instruction=self.prompt
            )
            chat = model.start_chat(
                history=[],
            )
            contents = self.get_contents(links)
            response = chat.send_message(contents)
            return self.get_site_keywords(response.text)
        except Exception as e:
            print(f"gemini response error: {e}")
            return []

    def run(self) -> List[str]:
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