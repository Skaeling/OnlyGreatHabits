from datetime import timedelta

from rest_framework.serializers import ValidationError

from habits.models import Habit


def validate_duration(value):
    if value > timedelta(seconds=120):
        raise ValidationError('Длительность действия не может превышать 120 секунд')


def validate_regularity(value):
    if value == 0 or value > 7:
        raise ValidationError('Периодичность привычки не может быть реже чем 1 раз в день/ 1 раз в неделю')


def validate_associated_habit(value):
    habit = Habit.objects.all().filter(pk=value.pk).first()
    if habit and not habit.is_pleasurable:
        raise ValidationError(
            'В связанные привычки могут попадать только привычки с признаком приятной привычки.')


# def validate_is_pleasurable(value, data):
#     if value and data['reward']:
#         raise ValidationError(
#             'У приятной привычки не может быть вознаграждения или связанной привычки.'
#         )
#
#
# def validate_reward(value):
#     """Исключить одновременный выбор связанной привычки и указания вознаграждения."""
#     pass