from dataclasses import dataclass

@dataclass
class SiteKeyword:
    date : str
    llm : str
    model : str
    name : str
    keyword : str
    point : int = 0
    id : int = 0

    def __hash__(self):
        return hash(f"{self.date}{self.llm}{self.model}{self.name}{self.keyword}") 

@dataclass
class SiteKeywordSum:
    date : str
    name : str
    keyword : str
    point : int = 0

    def __hash__(self):
        return hash(f"{self.date}{self.name}{self.keyword}") 