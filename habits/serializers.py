from rest_framework import serializers
from .models import Habit
from .validators import validate_duration, validate_regularity, validate_associated_habit, validate_is_pleasurable


class HabitSerializer(serializers.ModelSerializer):
    regularity = serializers.IntegerField(validators=[validate_regularity])
    duration = serializers.DurationField(validators=[validate_duration])
    associated_habit = serializers.PrimaryKeyRelatedField(
        queryset=Habit.objects.all(),
        validators=[validate_associated_habit]
    )
    # is_pleasurable = serializers.BooleanField(validators=[validate_is_pleasurable])

    class Meta:
        model = Habit
        exclude = ('user',)
