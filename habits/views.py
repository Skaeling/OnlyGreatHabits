from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsOwner
from .models import Habit
from .serializers import HabitSerializer, PublicHabitSerializer


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
