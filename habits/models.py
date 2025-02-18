from datetime import timedelta

from django.db import models
from config import settings


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    place = models.CharField(null=True, blank=True, max_length=50, verbose_name='Место действия')
    start_time = models.TimeField(default="12:00:00", verbose_name='Время начала выполнения')
    action = models.CharField(max_length=150, verbose_name='Описание действия')
    is_pleasurable = models.BooleanField(default=False, verbose_name='Приятная привычка')
    associated_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                         verbose_name="Связанная привычка")
    regularity = models.PositiveIntegerField(default=1, verbose_name='Периодичность в днях')
    reward = models.CharField(max_length=150, null=True, blank=True, verbose_name='Вознаграждение')
    duration = models.DurationField(default=timedelta(seconds=120), verbose_name='Длительность')
    is_public = models.BooleanField(default='False', verbose_name='Публичная')

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return f'Я буду {self.action} в {self.start_time} в {self.place}'
