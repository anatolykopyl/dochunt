from rich.console import Console
import calendar;
import time;
c = Console()
ts = calendar.timegm(time.gmtime())

def save_photo(url):
    f = open(f"output/{ts}.html", "a", encoding='utf-8')
    f.write(f'<img width=400 src="{url}"><br>')
    f.close()
    