from datetime import datetime
from app.score.link_title_score import LinkTitleScore
from app.data.database import init_db

cur_date = datetime.now().strftime("%Y%m%d")

def link_title_scoring():
    print("============================\nlink title scoring starting")
    LinkTitleScore(cur_date).run()

if __name__ == '__main__':
    init_db()
    link_title_scoring()