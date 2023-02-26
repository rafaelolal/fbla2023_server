from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Student, Leaderboard


class LeaderboardTests(APITestCase):

    def test_leaderboard_update_view(self):
        leaderboard = Leaderboard.objects.create(created_on='2022-02-24')
        student1 = Student.objects.create(
            id='1', email='student1@example.com', first_name='John', last_name='Doe',
            biography='Lorem ipsum', grade=7, live_points=10, points=0)
        student2 = Student.objects.create(
            id='2', email='student2@example.com', first_name='Jane', last_name='Doe',
            biography='Dolor sit', grade=8, live_points=5, points=0)

        url = reverse('leaderboard-update', kwargs={'pk': leaderboard.pk})
        response = self.client.put(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        leaderboard.refresh_from_db()
        self.assertEqual(str(leaderboard.created_on), str(date.today()))

        student1.refresh_from_db()
        student2.refresh_from_db()
        self.assertEqual(student1.rank, 1)
        self.assertEqual(student2.rank, 2)
        self.assertEqual(student1.points, 10)
        self.assertEqual(student2.points, 5)
