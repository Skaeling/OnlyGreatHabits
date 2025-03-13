from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTest(APITestCase):

    def setUp(self):
        self.some_user = User.objects.create(email="some_user@email.com", username="some_user")
        self.client.force_authenticate(user=self.some_user)
        self.public_habit = Habit.objects.create(action="медитировать", is_public=True, user=self.some_user)

        self.user = User.objects.create(email="user@email.com", username="user")
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(action="отжиматься", is_public=True, user=self.user)

    def test_habit_retrieve(self):
        """Тестирование детального отображения привычки"""

        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_create(self):
        """Тестирование создания привычки"""

        url = reverse("habits:habit-list")
        data = {"action": "отжиматься"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 3)

    def test_habit_update(self):
        """Тестирование обновления привычки"""

        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        data = {"start_time": "14:30:00"}
        response = self.client.patch(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get("start_time"), "14:30:00")

    def test_habit_delete(self):
        """Тестирование удаления привычки"""

        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 1)

    def test_habit_list(self):
        """Тестирование отображения пользователю списка собственных привычек"""

        url = reverse("habits:habit-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "regularity": 1,
                    "duration": "00:02:00",
                    "associated_habit": None,
                    "place": None,
                    "start_time": "12:00:00",
                    "action": self.habit.action,
                    "is_pleasurable": False,
                    "reward": None,
                    "is_public": True,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_public_habits_list(self):
        """Тестирование отображения текущему пользователю списка всех публичных привычек, исключая собственные"""

        url = reverse("habits:public_habits")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "action": self.public_habit.action,
                    "associated_habit": None,
                    "duration": "00:02:00",
                    "id": self.public_habit.pk,
                    "is_pleasurable": False,
                    "is_public": self.public_habit.is_public,
                    "place": None,
                    "regularity": 1,
                    "reward": None,
                    "start_time": "12:00:00",
                    "user": self.some_user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
