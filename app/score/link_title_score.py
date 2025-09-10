from app.data.database import (
    get_site_keywords, 
    reset_site_links, 
    update_site_link_rank, 
    get_all_site_links,
    delete_all_site_link_keyword,
    insert_into_site_link_keyword
)
from app.data.site_link import SiteLink
from app.data.site_keyword import SiteKeywordSum

class LinkTitleScore:
    def __init__(self, date):
        self.date = date

    def read_keywords(self):
        self.keywords_dict = {}
        keywords = get_site_keywords(self.date)
        for keyword in keywords:
            name_keyword = self.keywords_dict.get(keyword.name, {})
            name_keyword[keyword.keyword] = keyword.point
            self.keywords_dict[keyword.name] = name_keyword
        self.site_keywords = {}
        for key in self.keywords_dict.keys():
            self.site_keywords[key] = self.keywords_dict[key].keys()

    def set_site_link_point(self, site_link: SiteLink):
        point = 0
        if site_link.name in self.site_keywords:
            site_keywords = self.site_keywords[site_link.name]
            site_keyword_dic = self.keywords_dict.get(site_link.name, {})
            for site_keyword in site_keywords:
                if site_keyword in site_link.title:
                    insert_into_site_link_keyword(site_link.id, self.date, site_keyword)
                    point = point + site_keyword_dic.get(site_keyword, 0)

        update_site_link_rank(site_link.id, point)

    def do_site_link_point_setting(self):
        site_links = get_all_site_links(self.date)
        for site_link in site_links:
            self.set_site_link_point(site_link)

    def run(self):
        reset_site_links(self.date)
        delete_all_site_link_keyword(self.date)
        self.read_keywords()
        self.do_site_link_point_setting()
