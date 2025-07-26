from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Prize
from ..serializers.prize import PrizeSerializer


class PrizeAPITestCase(APITestCase):
    def test_create_prize(self):
        data = {'name': 'Test Name', 'type': 'School', 'cost': 10}
        url = reverse('prize-create')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Prize.objects.count(), 1)
        self.assertEqual(Prize.objects.get().type, 'School')
        self.assertEqual(Prize.objects.get().name, 'Test Name')
        self.assertEqual(Prize.objects.get().cost, 10)

        expected_data = PrizeSerializer(Prize.objects.get()).data
        self.assertEqual(response.data, expected_data)

    def test_list_prizes(self):
        prize1 = Prize.objects.create(name="Prize 1", type='School', cost=10)
        prize2 = Prize.objects.create(name="Prize 2", type='Food', cost=10)

        url = reverse('prize-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        expected_data = PrizeSerializer([prize1, prize2], many=True).data
        self.assertEqual(response.data, expected_data)
