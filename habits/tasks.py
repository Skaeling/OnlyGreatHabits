from celery import shared_task
import json
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from habits.models import Habit
from habits.services import check_time, send_message


@shared_task
def create_or_update_plan(pk):
    habit = Habit.objects.get(pk=pk)
    start = check_time(habit.start_time)
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=habit.regularity,
        period=IntervalSchedule.MINUTES,
    )

    task, not_updated = PeriodicTask.objects.update_or_create(
        name=f'Send habit №{habit.pk} to {habit.user.username}',
        defaults={
            'interval': schedule,
            'name': f'Send habit №{habit.pk} to {habit.user.username}',
            'task': 'habit.tasks.send_tg_notification',
            'args': json.dumps([habit.pk]),
            'start_time': start,
        }

    )
    if not_updated:
        return f'Routine plan for habit №{habit.pk} created'
    return f'Routine plan for habit №{habit.pk} updated'


@shared_task(name='habit.tasks.send_tg_notification')
def send_tg_notification(pk):
    habit = Habit.objects.get(pk=pk)
    place = " в " + habit.place if habit.place else ''
    message = f'<b>Напоминание о привычке<tg-emoji emoji-id="5368324170671202286">❗</tg-emoji></b>' \
              f'\n{habit.action.capitalize()}{place}, начать необходимо в {habit.start_time.strftime("%H:%M")}.'
    if habit.reward:
        message += f'\n\n<b>Ваша награда за выполнение<tg-emoji emoji-id="5368324170671202286">⭐</tg-emoji></b> \n{habit.reward.capitalize()}'
    elif habit.associated_habit:
        message += f'\n\n<b>Ваша приятная привычка после завершения<tg-emoji emoji-id="5368324170671202286">👍</tg-emoji>:</b> \n{habit.associated_habit.action.capitalize()}'
    # print(message)
    if habit.user.tg_chat_id:
        send_message(habit.user.tg_chat_id, message)
        return f"Notification sent to {habit.user.username}"
    return "No chat_id found"


@shared_task
def delete_plan(pk, username):
    PeriodicTask.objects.filter(name=f'Send habit №{pk} to {username}').delete()
