import time
import subprocess
from threading import Timer

def run_parser():
    try:
        subprocess.run(["python3", "rss_parser.py"], check=True)
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Перезапускаем каждые 30 минут (1800 секунд)
        Timer(1800, run_parser).start()


run_parser()
while True:
    time.sleep(1)  # Бесконечный циклp