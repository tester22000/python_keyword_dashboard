import sqlite3

from app.data.site_keyword import SiteKeyword, SiteKeywordSum
from app.data.site_link import SiteLink
from typing import List
import os

db = sqlite3.connect(os.getenv("SITE_LINK_SQLITE","./site_links.db"))

def init_db():
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS site_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            link TEXT NOT NULL,
            title TEXT NOT NULL,
            date VARCHAR(8) DEFAULT (strftime('%Y%m%d', 'now')),
            rank INTEGER DEFAULT 0
        )
    ''')
    cursor.execute(''' CREATE UNIQUE INDEX IF NOT EXISTS site_links_index1 ON site_links ( name, date, link ) ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS site_keywords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        llm VARCHAR(100) NOT NULL,
        model VARCHAR(100) NOT NULL,
        date VARCHAR(8) NOT NULL,
        name TEXT NOT NULL,
        keyword TEXT NOT NULL,
        point INTEGER DEFAULT 0
    )
    ''')
    cursor.execute(''' CREATE UNIQUE INDEX IF NOT EXISTS site_keywords_index1 ON site_keywords ( date, llm, model, name, keyword ) ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS site_link_keyword (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        link_id INTEGER NOT NULL,
        date VARCHAR(8) NOT NULL,
        keyword TEXT NOT NULL,
        FOREIGN KEY(link_id) REFERENCES site_links(id) ON DELETE CASCADE
    )
    ''')
    cursor.execute(''' CREATE UNIQUE INDEX IF NOT EXISTS site_link_keyword_index_1 ON site_link_keyword ( link_id, date, keyword ) ''')
    cursor.execute(''' CREATE INDEX IF NOT EXISTS site_link_keyword_index_2 ON site_link_keyword ( date ) ''')
    db.commit()


def insert_site_link(link: SiteLink):
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO site_links (name, link, title) VALUES (?, ?, ?)", (link.name, link.link, link.title))
        db.commit()
    except Exception as e:
        print(f"'{link}' 추가 실패: {e}")

def get_site_names(date:str) -> List[str]:
    result = []
    cursor = db.cursor()
    cursor.execute("SELECT distinct name as name from site_links where date = ?", [date])
    for row in cursor.fetchall():
        result.append(row[0])
    return result

def get_site_links(name:str, date:str) -> List[SiteLink]:
    result = []
    cursor = db.cursor()
    cursor.execute("SELECT * from site_links where name = ? and date = ?",(name, date))
    column_names = [description[0] for description in cursor.description] 
    for row_data in cursor.fetchall():
        row = dict(zip(column_names, row_data))
        result.append(SiteLink(
            id = row['id'],
            name = row['name'],
            link = row['link'],
            title = row['title'],
            date = row['date'],
            rank= row['rank']
        ))
    return result

def get_all_site_links(date:str) -> List[SiteLink]:
    result = []
    cursor = db.cursor()
    cursor.execute("SELECT * from site_links where date = ?",[date])
    column_names = [description[0] for description in cursor.description] 
    for row_data in cursor.fetchall():
        row = dict(zip(column_names, row_data))
        result.append(SiteLink(
            id = row['id'],
            name = row['name'],
            link = row['link'],
            title = row['title'],
            date = row['date'],
            rank= row['rank']
        ))
    return result

def delete_site_links(name:str, date:str):
    cursor = db.cursor()
    cursor.execute("DELETE from site_links where name = ? and date = ?",(name, date))
    db.commit()

def delete_all_site_links(date:str):
    cursor = db.cursor()
    cursor.execute("DELETE from site_links where date = ?",[date])
    db.commit()

def update_site_link_rank(id: int, rank: int):
    cursor = db.cursor()
    cursor.execute("UPDATE site_links set rank = ? where id  = ?",(rank, id))
    db.commit()

def reset_site_links(date:str):
    cursor = db.cursor()
    cursor.execute("UPDATE site_links set rank = 0 where date = ?",[date])
    db.commit()


def insert_site_keyword(keyword: SiteKeyword):
    try:
        cursor = db.cursor()
        cursor.execute("INSERT OR IGNORE INTO site_keywords (date, name, llm, model, keyword, point) VALUES (?, ?, ?, ?, ?, ?)", (
            keyword.date, 
            keyword.name, 
            keyword.llm, 
            keyword.model, 
            keyword.keyword, 
            keyword.point))
        db.commit()
    except Exception as e:
        print(f"'{keyword}' 추가 실패: {e}")



def get_site_keywords(date:str) -> List[SiteKeywordSum]:
    result = []
    cursor = db.cursor()
    cursor.execute("SELECT date, name, keyword, sum(point) as point from site_keywords where date = ? group by date, name, keyword",[date])
    column_names = [description[0] for description in cursor.description] 
    for row_data in cursor.fetchall():
        row = dict(zip(column_names, row_data))
        result.append(SiteKeywordSum(
            date = row['date'],
            name = row['name'],
            keyword = row['keyword'],
            point = row['point']
        ))
    return result


def delete_site_keywords(name:str, date:str):
    cursor = db.cursor()
    cursor.execute("DELETE from site_keywords where name = ? and date = ?",(name, date))
    db.commit()

def delete_all_site_keywords(date:str):
    cursor = db.cursor()
    cursor.execute("DELETE from site_keywords where date = ?",[date])
    db.commit()


def insert_into_site_link_keyword(link_id, date, keyword):
    try:
        cursor = db.cursor()
        cursor.execute("INSERT OR IGNORE INTO site_link_keyword (link_id, date, keyword) VALUES (?, ?, ?)", (
            link_id, 
            date, 
            keyword))
        db.commit()
    except Exception as e:
        print(f"'{keyword}' 추가 실패: {e}")

def delete_all_site_link_keyword(date):
    cursor = db.cursor()
    cursor.execute("DELETE from site_link_keyword where date = ?",[date])
    db.commit()