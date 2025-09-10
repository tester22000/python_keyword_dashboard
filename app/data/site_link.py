from dataclasses import dataclass
import datetime

@dataclass
class SiteLink:
    name : str
    link : str
    title : str
    id : int = 0
    date : str = datetime.datetime.now().strftime("%Y%m%d")
    rank :int = 0