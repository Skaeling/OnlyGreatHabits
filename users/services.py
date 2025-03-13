import requests

from config.settings import TG_URL, TG_KEY


def get_user_chat_id():
    """Возвращает chat_id пользователя, в случае ошибки запроса возвращает None"""
    chat_id = None
    try:
        response = requests.get(f'{TG_URL}{TG_KEY}/getUpdates?offset=-1')
        response.raise_for_status()
        chat_id = response.json()['result'][0]['message']['chat']['id']
    except (requests.exceptions.RequestException, KeyError, IndexError):
        pass
    return chat_id
