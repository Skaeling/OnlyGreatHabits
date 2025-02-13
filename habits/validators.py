from datetime import timedelta

from rest_framework.serializers import ValidationError


def validate_duration(value):
    if value > timedelta(seconds=120):
        raise ValidationError('Длительность действия не может превышать 120 секунд')


def validate_regularity(value):
    if value == 0 or value > 7:
        raise ValidationError('Периодичность привычки не может быть реже чем 1 раз в день/ 1 раз в неделю')


class AssociatedHabitValidator:

    def __init__(self, is_pleasurable, associated_habit, reward):
        self.is_pleasurable = is_pleasurable
        self.associated_habit = associated_habit
        self.reward = reward

    def __call__(self, value):
        associated_habit = value.get(self.associated_habit)
        is_pleasurable = value.get(self.is_pleasurable)
        reward = value.get(self.reward)

        if associated_habit and not associated_habit.is_pleasurable:
            raise ValidationError(
                'В связанные привычки могут попадать только привычки с признаком приятной привычки.'
            )
        if is_pleasurable and (associated_habit or reward):
            raise ValidationError(
                'У приятной привычки не может быть связанной привычки и вознаграждения.'
            )
        if reward and associated_habit:
            raise ValidationError(
                'Можно выбрать либо вознаграждение, либо связанную привычку'
            )
