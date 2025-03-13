from rest_framework import serializers

from .models import User
from .services import get_user_chat_id


class UserSerializer(serializers.ModelSerializer):
    tg_chat_id = serializers.CharField(required=False, default=get_user_chat_id())

    class Meta:
        model = User
        fields = '__all__'
