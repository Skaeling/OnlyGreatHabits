from rest_framework import serializers
from .models import Habit
from .validators import validate_duration, validate_regularity, AssociatedHabitValidator


class HabitSerializer(serializers.ModelSerializer):
    regularity = serializers.IntegerField(validators=[validate_regularity], required=False)
    duration = serializers.DurationField(validators=[validate_duration], required=False)
    associated_habit = serializers.PrimaryKeyRelatedField(queryset=Habit.objects.all(), allow_empty=True, required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    validators = [AssociatedHabitValidator('is_pleasurable', 'associated_habit', 'reward')]

    def validate(self, data):
        if data.get('is_pleasurable') is False and (data.get('regularity') is None or data.get('duration') is None):
            raise serializers.ValidationError(
                "Для полезной привычки обязательны для заполнения поля 'regularity' и 'duration'.")
        return data

    class Meta:
        model = Habit
        fields = '__all__'
