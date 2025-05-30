# =============================================
#  Rss парсер новостей
# =============================================
# Отслеживание ключевых слов в RSS-лентах. Сохранение в БД. Веб-интерфейс.

# ---------------------------------------------
# Структура проекта
# ---------------------------------------------
# .
# ├── Results and logs     # Результаты работы в pdf и логи из терминала
# ├── app.py               # Веб-сервис на Flask
# ├── rss_parser.py        # Парсер RSS-лент
# ├── init_db.py           # Инициализация БД SQLite
# ├── requirements.txt     # Зависимости
# └── templates
#     └── index.html       # Шаблон отображения новостей

# ---------------------------------------------
# Зависимости
# ---------------------------------------------
# feedparser==6.0.10
# Flask==3.0.2

# ---------------------------------------------
# Установка 
# ---------------------------------------------
git clone https://github.com/ваш_логин/rss-monitor.git
cd rss-monitor

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка библиотек
pip install -r requirements.txt

# Инициализация БД
python init_db.py

# ---------------------------------------------
# Запуск
# ---------------------------------------------
# Запуск веб-сервиса (в фоне):
python app.py &           # http://localhost:5000

# Ручной запуск парсера:
python rss_parser.py

# ---------------------------------------------
# Примеры добавления RSS-источников
# ---------------------------------------------
# Международные новости:
curl -X POST -F "url=http://feeds.bbci.co.uk/news/world/rss.xml" http://localhost:5000/add_source
curl -X POST -F "url=https://rss.nytimes.com/services/xml/rss/nyt/World.xml" http://localhost:5000/add_source

# ---------------------------------------------
# 🔑 Примеры ключевых слов
# ---------------------------------------------
curl -X POST -F "keyword=fire" http://localhost:5000/add_keyword
curl -X POST -F "keyword=cyber" http://localhost:5000/add_keyword
curl -X POST -F "keyword=Ukraine" http://localhost:5000/add_keyword
curl -X POST -F "keyword=crime" http://localhost:5000/add_keyword

# ---------------------------------------------
# Автозапуск парсера
# ---------------------------------------------
crontab -e
# Добавьте строку:
*/30 * * * * /полный/путь/к/python /полный/путь/к/rss_parser.py >> parser.log 2>&1

# ---------------------------------------------
# Веб-интерфейс
# ---------------------------------------------
# Доступен по адресу: http://localhost:5000

# API-эндпоинты:
# GET /          - Веб-интерфейс
# GET /news      - Новости в формате JSON
# POST /add_source - Добавить RSS-источник
# POST /add_keyword - Добавить ключевое слово

# ---------------------------------------------
# Логи и отладка
# ---------------------------------------------
# Просмотр логов парсера:
tail -f parser.log

# Проверка источников:
curl http://localhost:5000/sources

# Проверка ключевых слов:
curl http://localhost:5000/keywords

# ---------------------------------------------
# 📄 Лицензия: MIT
# ---------------------------------------------
