from rich.console import Console
c = Console()

def save_photo(url):
    f = open("output.txt", "a", encoding='utf-8')
    f.write(url)
    f.close()
    