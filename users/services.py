import requests

from config.settings import TG_URL, TG_KEY


def get_user_chat_id():
    response = requests.get(f'{TG_URL}{TG_KEY}/getUpdates')
    chat_id = response.json()['result'][0]['message']['chat']['id']
    return chat_id
