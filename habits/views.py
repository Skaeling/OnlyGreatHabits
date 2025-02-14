from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsOwner
from .models import Habit
from .serializers import HabitSerializer, PublicHabitSerializer
from .tasks import create_plan


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)
        if not habit.is_pleasurable:
            create_plan.delay(habit.pk)

    def get_queryset(self):
        if self.action == 'list':
            return Habit.objects.filter(user=self.request.user)
        return Habit.objects.all()

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = (IsOwner,)
        return super().get_permissions()


class HabitPublicListAPIView(generics.ListAPIView):
    serializer_class = PublicHabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
