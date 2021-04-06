import vk_api
import configparser
from rich.console import Console
c = Console()

config = configparser.ConfigParser()
config.read('config.ini')
login = config['CREDENTIALS']['login']
password = config['CREDENTIALS']['password']

def _2fa_handler():
    code = c.input("Enter 2FA code: ", style="italic cyan")
    return code, True

def authenticate():
    vk_session = vk_api.VkApi(login=login, password=password, auth_handler=_2fa_handler)
    vk_session.auth()
    c.print('Authentication success!', style='blue')

    return vk_session.get_api()