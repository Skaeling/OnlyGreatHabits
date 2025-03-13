from celery import shared_task
import json
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from habits.models import Habit
from habits.services import check_time, send_message


@shared_task
def create_or_update_plan(pk):
    """Создает план отправки напоминаний при его отсутствии или обновляет имеющийся"""

    habit = Habit.objects.get(pk=pk)
    start = check_time(habit.start_time)
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=habit.regularity,
        period=IntervalSchedule.MINUTES,
    )

    task, not_updated = PeriodicTask.objects.update_or_create(
        name=f"Send habit №{habit.pk} to {habit.user.username}",
        defaults={
            "interval": schedule,
            "name": f"Send habit №{habit.pk} to {habit.user.username}",
            "task": "habit.tasks.send_tg_notification",
            "args": json.dumps([habit.pk]),
            "start_time": start,
        },
    )
    if not_updated:
        return f"Routine plan for habit №{habit.pk} created"
    return f"Routine plan for habit №{habit.pk} updated"


@shared_task(name="habit.tasks.send_tg_notification")
def send_tg_notification(pk):
    """Собирает текст напоминания и отправляет пользователю в Телеграм с заданной периодичностью при наличии chat_id"""

    habit = Habit.objects.get(pk=pk)
    place = " в " + habit.place if habit.place else ""
    message = (
        f'<b>Напоминание о привычке<tg-emoji emoji-id="5368324170671202286">❗</tg-emoji></b>'
        f'\n{habit.action.capitalize()}{place}, начать необходимо в {habit.start_time.strftime("%H:%M")}.'
    )
    if habit.reward:
        message += f'\n\n<b>Ваша награда за выполнение' \
                   f'<tg-emoji emoji-id="5368324170671202286">⭐</tg-emoji></b> ' \
                   f'\n{habit.reward.capitalize()}'
    elif habit.associated_habit:
        message += f'\n\n<b>Ваша приятная привычка после завершения' \
                   f'<tg-emoji emoji-id="5368324170671202286">👍</tg-emoji></b> ' \
                   f'\n{habit.associated_habit.action.capitalize()}'

    if not habit.user.tg_chat_id:
        # возможна дополнительная логика: при отсутствии chat_id пользователю приходит письмо с напоминанием на почту
        return "Уведомление не отправлено, не указан chat_id"

    if send_message(habit.user.tg_chat_id, message):
        return f"Уведомление пользователю {habit.user.username} отправлено"
    return 'Ошибка при отправке уведомления'


@shared_task
def delete_plan(pk, username):
    PeriodicTask.objects.filter(name=f"Send habit №{pk} to {username}").delete()
