import sqlite3

conn = sqlite3.connect('news.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS keywords (
    id INTEGER PRIMARY KEY,
    keyword TEXT NOT NULL UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    link TEXT NOT NULL UNIQUE,
    source_id INTEGER,
    published_date DATETIME,
    FOREIGN KEY (source_id) REFERENCES sources(id)
)
''')

conn.commit()
conn.close()