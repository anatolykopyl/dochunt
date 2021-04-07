import vk_api
import configparser
from rich.console import Console
from rich.prompt import Prompt
c = Console()

config = configparser.ConfigParser()
config.read('config.ini')
login = config['CREDENTIALS']['login']
password = config['CREDENTIALS']['password']

def _2fa_handler():
    code = Prompt.ask("Enter 2FA code")
    return code, True

def authenticate():
    vk_session = vk_api.VkApi(login=login, password=password, auth_handler=_2fa_handler)
    vk_session.auth()
    c.print('Authentication success!', style='blue')

    return vk_session.get_api()