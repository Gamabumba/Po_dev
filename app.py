from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT news.title, news.content, news.link, sources.url 
        FROM news 
        INNER JOIN sources ON news.source_id = sources.id
    ''')
    news_items = cursor.fetchall()
    conn.close()
    return render_template('index.html', news_items=news_items)

@app.route('/news', methods=['GET'])
def get_news():
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, content, link FROM news')
    news = [{'title': row[0], 'content': row[1], 'link': row[2]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(news)

@app.route('/add_source', methods=['POST'])
def add_source():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO sources (url) VALUES (?)', (url,))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Source already exists'}), 400
    finally:
        conn.close()
    return jsonify({'message': 'Source added'})

@app.route('/add_keyword', methods=['POST'])
def add_keyword():
    keyword = request.form.get('keyword')
    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400

    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO keywords (keyword) VALUES (?)', (keyword.lower(),))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Keyword exists'}), 400
    finally:
        conn.close()
    return jsonify({'message': 'Keyword added'})

@app.route('/sources', methods=['GET'])
def get_sources():
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, url FROM sources')
    sources = [{'id': row[0], 'url': row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(sources)

@app.route('/keywords', methods=['GET'])
def get_keywords():
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, keyword FROM keywords')
    keywords = [{'id': row[0], 'keyword': row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(keywords)

if __name__ == '__main__':
    app.run(debug=True)