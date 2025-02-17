from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsOwner
from .models import Habit
from .serializers import HabitSerializer, PublicHabitSerializer
from .tasks import create_or_update_plan, delete_plan


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)
        if not habit.is_pleasurable:
            create_or_update_plan.apply_async(args=(habit.pk,), countdown=30)

    def get_queryset(self):
        if self.action == 'list':
            return Habit.objects.filter(user=self.request.user)
        return Habit.objects.all()

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = (IsOwner,)
        return super().get_permissions()

    def perform_update(self, serializer):
        initial_data = serializer.initial_data
        instance = serializer.save()
        if any(initial_data.get(field) != getattr(instance, field) for field in ('start_time', 'regularity')):
            create_or_update_plan.apply_async(args=(instance.pk,), countdown=30)

    def perform_destroy(self, instance):
        delete_plan.delay(instance.pk, instance.user.username)
        instance.delete()


class HabitPublicListAPIView(generics.ListAPIView):
    serializer_class = PublicHabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
