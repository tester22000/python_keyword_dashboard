import yaml
from datetime import datetime, timedelta

from app.data import database
from app.data.site_link import SiteLink
from app.extractor.base_collector import BaseExtractor
from app.extractor.ollama_keyword_extractor import OllamaKeywordExtractor
from app.extractor.gemini_keyword_extractor import GeminiKeywordExtractor

cur_date = datetime.now().strftime("%Y%m%d")

def load_llm_config(config_file:str):
    with open(config_file, encoding='utf-8') as f:
        data = yaml.safe_load(f)
        return data['llms']

def get_extractors(config_file:str):
    extractors = []
    llm_configs = load_llm_config(config_file)

    sites = database.get_site_names(cur_date)
    collection_tasks = []
    for site in sites:
        links = database.get_site_links(site, cur_date)
        for llm_config in llm_configs:
            model = llm_config['model']
            chunk = int(llm_config['chunk'])
            prompt = llm_config['prompt_template']
            if llm_config['enable']:
                if llm_config['type'] == 'ollama':
                    collection_tasks.append(OllamaKeywordExtractor(cur_date, model, site, prompt, links, chunk))
                elif llm_config['type'] == 'gemini':
                    collection_tasks.append(GeminiKeywordExtractor(cur_date, model, site, prompt, links, chunk))
                    pass

    return collection_tasks    


def run_extract_task(task: BaseExtractor):
    results = task.run()
    for result in results:
        database.insert_site_keyword(result)
    return results


def extract_keywords(config_file:str):
    print("============================\nExtract keyword using llm starting")
    database.init_db()
    database.delete_all_site_keywords(cur_date)
    tasks = get_extractors(config_file)

    results = []
    for task in tasks:
        results.extend(run_extract_task(task))

if __name__ == '__main__':
    extract_keywords('../config/llm_config.yaml')