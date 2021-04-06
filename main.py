import configparser
import ast
from time import sleep
from rich import print#, inspect
from rich.console import Console

from utils.authenticate import authenticate
from utils.detect import detect

config = configparser.ConfigParser()
config.read('config.ini')
terms = ast.literal_eval(config['SEARCH']['terms'])
interests = ast.literal_eval(config['SEARCH']['interests'])

c = Console()
vk = authenticate()

queries = []
for i in range(len(terms)):
    queries.append({
        'string': terms[i],
        'last_url': ''
    })

photos_processed = 0
photos_saved = 0
while True:
    for query in queries:
        response = vk.docs.search(q=query['string'], count=1)
        image_url = response.popitem()[1][0]['url'] # WTF not readable
        image_url_clean = image_url.split('?')[0] # Get url without params

        # If the image we are getting is new do stuff
        if image_url_clean != query['last_url']:
            photos_processed += 1
            query['last_url'] = image_url_clean

            text = detect(image_url+query['string'])
            for interest in interests:
                if interest in text:
                    photos_saved += 1
                    c.print('Found an interesting photo!', style="green")
                    c.print(image_url)

        sleep(1)
