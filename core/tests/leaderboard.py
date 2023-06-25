from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Student, Leaderboard
from ..serializers.leaderboard import LeaderboardRetrieveSerializer


class LeaderboardTests(APITestCase):

    def test_retrieve_leaderboard(self):
        leaderboard = Leaderboard.objects.create()

        url = reverse('leaderboard-retrieve', kwargs={'id': 1})
        serializer = LeaderboardRetrieveSerializer(leaderboard)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_leaderboard_update_view(self):
        leaderboard = Leaderboard.objects.create(created_on='2022-02-24')
        student1 = Student.objects.create(
            id='1', email='student1@example.com', first_name='John', last_name='Doe',
            biography='Lorem ipsum', grade=7, balance=10, current_points=0)
        student2 = Student.objects.create(
            id='2', email='student2@example.com', first_name='Jane', last_name='Doe',
            biography='Dolor sit', grade=8, balance=5, current_points=0)

        url = reverse('leaderboard-update', kwargs={'id': leaderboard.id})
        response = self.client.put(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        leaderboard.refresh_from_db()
        self.assertEqual(str(leaderboard.created_on), str(date.today()))

        student1.refresh_from_db()
        student2.refresh_from_db()
        self.assertEqual(student1.rank, 1)
        self.assertEqual(student2.rank, 2)
        self.assertEqual(student1.current_points, 10)
        self.assertEqual(student2.current_points, 5)
