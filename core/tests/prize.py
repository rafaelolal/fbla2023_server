from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Student, Prize
from ..serializers.prize import PrizeSerializer


class PrizeAPITestCase(APITestCase):
    def test_create_prize(self):
        student = Student.objects.create(
            id='1', email='test@test.com', first_name='John', last_name='Doe'
        )
        data = {'type': 'School', 'student': student.id}
        url = reverse('prize-create')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Prize.objects.count(), 1)
        self.assertEqual(Prize.objects.get().type, 'School')
        self.assertEqual(Prize.objects.get().student.id, student.id)

        expected_data = PrizeSerializer(Prize.objects.get()).data
        self.assertEqual(response.data, expected_data)

    def test_list_prizes(self):
        student = Student.objects.create(
            id='student1id', email='test@test.com', first_name='John', last_name='Doe'
        )
        prize1 = Prize.objects.create(type='School', student=student)
        prize2 = Prize.objects.create(type='Food', student=student)

        url = reverse('prize-list', kwargs={'student': student.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        expected_data = PrizeSerializer([prize1, prize2], many=True).data
        self.assertEqual(response.data, expected_data)
