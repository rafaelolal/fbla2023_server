from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import Admin
from ..serializers.admin import AdminSerializer


class AdminAPITestCase(APITestCase):
    def test_admin_create(self):
        url = reverse('admin-create')
        data = {'pk': 'admin1'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Admin.objects.count(), 1)
        self.assertEqual(Admin.objects.get().pk, 'admin1')
        self.assertEqual(response.data, {'pk': 'admin1'})

    def test_admin_retrieve(self):
        admin = Admin.objects.create(pk='admin1')
        url = reverse('admin-retrieve', args=[admin.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'pk': 'admin1'})
