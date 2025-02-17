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
    message = f'Напоминание о привычке #{habit.pk}: ' \
              f'{habit.action} в {habit.place}, начать необходимо в {habit.start_time.strftime("%H:%M")}.'
    if habit.reward:
        message += f' \nВаша награда за выполнение: {habit.reward}'
    elif habit.associated_habit:
        message += f' \nВаша приятная привычка после завершения: {habit.associated_habit.action}'
    # print(message)
    if habit.user.tg_chat_id:
        send_message(habit.user.tg_chat_id, message)
    else:
        print("No chat_id found")


@shared_task
def delete_plan(pk, username):
    PeriodicTask.objects.filter(name=f'Send habit №{pk} to {username}').delete()
