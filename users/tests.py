from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTest(APITestCase):

    def test_user_create(self):
        """Тестирование создания юзера"""

        url = reverse("users:register")
        data = {"email": "user@email.com", "username": "user", "password": 12345}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 1)
