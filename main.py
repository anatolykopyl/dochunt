import configparser
import argparse 
import ast
import sys
from time import sleep
from rich import print#, inspect
from rich.console import Console

from utils.authenticate import authenticate
from utils.detect import detect
from utils.savePhoto import save_photo

config = configparser.ConfigParser()
config.read('config.ini')
terms = ast.literal_eval(config['SEARCH']['terms'])
if config['SEARCH']['interests'] != "all":
    interests = ast.literal_eval(config['SEARCH']['interests'])
else:
    interests = "all"

parser = argparse.ArgumentParser(description='Get documents from vk.com')
parser.add_argument('-a', '--all', action='store_true', 
    help='Search through all availible documents instead of watching only the most recent uploads.')
args = parser.parse_args()

def update_status():
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    c.print(f'> Documents scanned {photos_processed}')
    c.print(f'> Documents saved {photos_saved}')

c = Console()
c.print('[b]Dochunt[/b] starting...', style='yellow')
vk = authenticate()

queries = []
for i in range(len(terms)):
    queries.append({
        'string': terms[i],
        'last_url': '',
        'completed': False
    })

photos_processed = 0
photos_saved = 0

c.print('Watching documents :eyes:', style='italic')
c.print(f'> Documents scanned {photos_processed}')
c.print(f'> Documents saved {photos_saved}')
while True:
    try:
        for query in queries:
            if args.all and not query['completed']:
                response = vk.docs.search(q=query['string'], count=1000)
            else:
                response = vk.docs.search(q=query['string'], count=1)
            
            pics_array = response.popitem()[1]
            for pic in pics_array:
                image_url = pic['url'] # WTF not readable
                image_url_clean = image_url.split('?')[0] # Get url without params

                # If the image we are getting is new do stuff
                if image_url_clean != query['last_url']:
                    photos_processed += 1
                    update_status()
                    query['last_url'] = image_url_clean

                    text = detect(image_url+query['string'])
                    if interests == "all":
                        if not text.isspace():
                            photos_saved += 1
                            save_photo(image_url)
                    else:
                        for interest in interests:
                            if interest in text:
                                photos_saved += 1
                                save_photo(image_url)

            sleep(1)
    
    except KeyboardInterrupt:
        c.print(' Goodbye!', style='blue')
        sys.exit()
