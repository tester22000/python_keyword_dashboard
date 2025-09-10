import sqlite3
import os

DATABASE = 'database.db'

def get_db_connection():
    """데이터베이스 연결 객체를 반환합니다."""
    conn = sqlite3.connect(os.getenv("SITE_LINK_SQLITE","./site_links.db"))
    conn.row_factory = sqlite3.Row
    return conn

def get_site_links(page, limit, name=None, keyword=None, date=None, search=None):
    """
    조건에 맞는 site_links 데이터를 페이징하여 조회합니다.
    - 무한 스크롤 기능에 사용됩니다.
    - name, keyword, date 조건에 따라 동적으로 쿼리를 생성합니다.
    """
    conn = get_db_connection()
    offset = (page - 1) * limit
    
    params = []
    if keyword:
        query = """
        SELECT a.id, a.name, a.link, a.title, a.date, a.rank FROM site_links a 
        join site_link_keyword b on a.id = b.link_id and b.keyword = ?
        WHERE 1=1
        """
        params.append(keyword)
    else:
        query = "SELECT a.id, a.name, a.link, a.title, a.date, a.rank FROM site_links a WHERE 1=1"
    if date:
        query += " AND a.date = ?"
        params.append(date)
    if name:
        query += " AND a.name = ?"
        params.append(name)
    if search:
        # title 필드에 대해 LIKE 검색을 수행합니다.
        query += " AND a.title LIKE ?"
        params.append(f'%{search}%')
    
    query += " ORDER BY a.rank DESC, a.id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    links = conn.execute(query, params).fetchall()
    conn.close()
    
    return [dict(link) for link in links]

def get_distinct_site_names(date):
    conn = get_db_connection()
    links = conn.execute("SELECT DISTINCT name FROM site_links WHERE date = ?", (date,)).fetchall()
    conn.close()
    return [dict(link) for link in links]


def get_site_keywords(name=None, keyword=None, date=None):

    conn = get_db_connection()
    query = "SELECT keyword, sum(point) as point FROM site_keywords WHERE 1=1"
    params = []

    if date:
        query += " AND date = ?"
        params.append(date)
    
    if name:
        query += " AND name = ?"
        params.append(name)
    
    if keyword:
        query += " AND keyword LIKE ?"
        params.append(f'%{keyword}%')
        
    query += " GROUP BY keyword"
    query += " ORDER BY point DESC LIMIT 20"

    keywords = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(k) for k in keywords]



def delete_site_links(link_ids):
    """
    주어진 ID 목록에 해당하는 site_links 데이터를 삭제합니다.
    - 체크박스 선택 후 삭제 기능에 사용됩니다.
    """
    conn = get_db_connection()
    try:
        # IN 절을 사용한 동적 쿼리 생성
        placeholders = ','.join('?' for _ in link_ids)
        query = f"DELETE FROM site_links WHERE id IN ({placeholders})"
        conn.execute(query, link_ids)
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_all_keywords():
    """
    site_keywords 테이블의 모든 키워드를 조회합니다.
    """
    conn = get_db_connection()
    keywords = conn.execute("SELECT keyword, point FROM site_keywords ORDER BY point DESC").fetchall()
    conn.close()
    return [dict(k) for k in keywords]