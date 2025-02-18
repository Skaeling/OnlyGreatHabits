from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.services import get_user_chat_id
from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    """Регистрирует профиль пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True, tg_chat_id=get_user_chat_id())
        user.set_password(user.password)
        user.save()
