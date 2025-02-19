import requests
from django.utils import timezone
from datetime import datetime, timedelta

from config.settings import TG_KEY, TG_URL


def check_time(start_time):
    """Возвращает datetime старта задачи, проверяя прошло ли указанное пользователем время начала в текущих сутках,
    если да - переносит старт задачи на следующий день в то же время"""
    today = timezone.now().date()
    date_obj = datetime.combine(today, start_time)
    tz_start = date_obj.astimezone(timezone.get_default_timezone())
    if tz_start < timezone.now():
        tz_start += timedelta(days=1)
    return tz_start


def send_message(chat_id, message):
    """Отправляет сообщение пользователю через бот Telegram"""
    params = {
        'text': message,
        'chat_id': chat_id,
        'parse_mode': 'HTML',
    }
    response = requests.get(f'{TG_URL}{TG_KEY}/sendMessage', params=params)
    if response.status_code != 200:
        print(f"Ошибка при отправке запроса: {response.status_code}")
        return False

    data = response.json()
    if not data["ok"]:
        print(f"Ошибка в параметрах запроса: {data['description']}")
        return False

    return True
