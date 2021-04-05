import argparse
import configparser
from PIL import Image
import pytesseract
import vk_api
from rich import print
from rich.console import Console
c = Console()

config = configparser.ConfigParser()
config.read('config.ini')
login = config['DEFAULT']['login']
password = config['DEFAULT']['password']

parser = argparse.ArgumentParser(description='List the content of a folder')

parser.add_argument('-l', '--login', action='store', help='Your vk login (phone or email)')
parser.add_argument('-p', '--password', action='store', help='Your vk password')

args = parser.parse_args()

def _2fa_handler():
    code = c.input("Enter 2FA code: ", style="bold cyan")
    return code, True

vk_session = vk_api.VkApi(login=args.login, password=args.password, auth_handler=_2fa_handler)
vk_session.auth()

vk = vk_session.get_api()

c.print(vk.docs.search(q=".jpg"))

#print(pytesseract.image_to_string(Image.open("test.png")))
