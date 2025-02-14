from celery import shared_task
import json
from datetime import datetime

from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from habits.models import Habit


@shared_task
def create_plan(pk):
    habit = Habit.objects.get(pk=pk)
    today = timezone.now().today().date()
    time_obj = datetime.combine(today, habit.start_time)
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=habit.regularity,
        period=IntervalSchedule.MINUTES,
    )
    PeriodicTask.objects.create(
        interval=schedule,
        name=f'Send telegram message {habit.pk}',
        task='habit.tasks.send_tg_notification',
        args=json.dumps([habit.pk]),
        # expires=timezone.now().today() + timedelta(minutes=30),
        start_time=time_obj.strftime("%Y-%m-%d %H:%M:%S"),
    )


@shared_task(name='habit.tasks.send_tg_notification')
def send_tg_notification(pk):
    habit = Habit.objects.get(pk=pk)
    message = f'Я буду {habit.action} в {habit.start_time} в {habit.place}'
    print(message)
