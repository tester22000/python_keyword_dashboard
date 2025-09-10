import yaml
from datetime import datetime, timedelta

from app.collector import OenPageLinkTitleCollector, PagingLinkTitleCollector, BaseCollector, LinkTitle
from app.data import database
from app.data.site_link import SiteLink
from datetime import datetime, timedelta

cur_date = datetime.now().strftime("%Y%m%d")

def load_link_title_sources(config_yaml:str):
    with open(config_yaml, encoding='utf-8') as f:
        data = yaml.safe_load(f)
        return data['sources']

def get_collectors(config_yaml:str):
    url_sources = load_link_title_sources(config_yaml)
    collection_tasks = []
    for source in url_sources:
        collector_name = source['type']
        
        if collector_name == "one_page_link_title_collector":
            collector = OenPageLinkTitleCollector(
                source['name'], 
                source['url'], 
                source['keyword'],
                source['exclude'])
            collection_tasks.append(collector)
        elif collector_name == "paging_link_title_collector":
            collector = PagingLinkTitleCollector(
                source['name'], 
                source['url'], 
                source['page_template'], 
                source['page_count'], 
                source['a_selector'], 
                source['rate_limit'],
                source['exclude'])
            collection_tasks.append(collector)
        else:
            raise ValueError(f"Unknown collector type: {collector_name}")
        
    return collection_tasks    


def run_collector_task(task: BaseCollector):
    results = task.run()
    for result in results:
        database.insert_site_link(SiteLink(
            name = result.name,
            link = result.link,
            title = result.title
        ))
    return results


def collect_titles(config_yaml:str):
    print("============================\ncollect site link starting")
    database.init_db()
    collect_tasks = get_collectors(config_yaml)

    results = []
    for collector in collect_tasks:
        results.extend(run_collector_task(collector))

if __name__ == '__main__':
    collect_titles('../config/site_source.yaml')