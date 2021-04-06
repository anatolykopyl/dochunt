import configparser
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

c = Console()
c.print('[b]Dochunt[/b] starting...', style='yellow')
vk = authenticate()

queries = []
for i in range(len(terms)):
    queries.append({
        'string': terms[i],
        'last_url': ''
    })

photos_processed = 0
photos_saved = 0

c.rule()
c.print('Watching documents :eyes:')
c.print(f'> Documents scanned {photos_processed}')
c.print(f'> Documents saved {photos_saved}')
while True:
    try:
        for query in queries:
            response = vk.docs.search(q=query['string'], count=1)
            image_url = response.popitem()[1][0]['url'] # WTF not readable
            image_url_clean = image_url.split('?')[0] # Get url without params

            # If the image we are getting is new do stuff
            if image_url_clean != query['last_url']:
                photos_processed += 1
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
            
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            c.print(f'> Documents scanned {photos_processed}')
            c.print(f'> Documents saved {photos_saved}')

            sleep(1)
    
    except KeyboardInterrupt:
        c.print('Goodbye!', style='blue')
        sys.exit()