import feedparser
import sqlite3
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)


def parse_feeds():
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT id, url FROM sources')
        sources = cursor.fetchall()
        logging.info(f"Found {len(sources)} RSS sources to check")

        cursor.execute('SELECT keyword FROM keywords')
        keywords = [row[0].lower() for row in cursor.fetchall()]
        logging.info(f"Tracking keywords: {', '.join(keywords)}")

        for source_id, url in sources:
            logging.info(f"Checking source: {url}")

            try:
                feed = feedparser.parse(url)
                if feed.bozo:
                    logging.warning(f"Error parsing feed: {feed.bozo_exception}")
                    continue

                new_entries = 0
                for entry in feed.entries:
                    title = entry.get('title', '')
                    content = entry.get('description', '')
                    link = entry.get('link', '')
                    published = entry.get('published_parsed')
                    published_date = datetime(*published[:6]) if published else None

                    text = (title + ' ' + content).lower()
                    found = any(keyword in text for keyword in keywords)

                    if found:
                        cursor.execute('SELECT id FROM news WHERE link = ?', (link,))
                        if not cursor.fetchone():
                            cursor.execute('''
                                INSERT INTO news (title, content, link, source_id, published_date)
                                VALUES (?, ?, ?, ?, ?)
                            ''', (title, content, link, source_id, published_date))
                            new_entries += 1
                            logging.info(f"New match: [{title}] ({link})")

                conn.commit()
                logging.info(f"Added {new_entries} new entries from {url}")

            except Exception as e:
                logging.error(f"Error processing {url}: {str(e)}")

    finally:
        conn.close()
        logging.info("Database connection closed")


if __name__ == '__main__':
    parse_feeds()