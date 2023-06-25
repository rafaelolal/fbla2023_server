from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import datetime, timedelta
from ..models import Rally
from ..serializers.rally import RallySerializer


class RallyTests(APITestCase):
    def test_retrieve_student(self):
        rally = Rally.objects.create(starts_on=datetime.now(tz=timezone.utc))

        url = reverse('rally-retrieve', kwargs={'id': 1})
        serializer = RallySerializer(rally)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_rally_starts_on(self):
        now = datetime.now(tz=timezone.utc)
        rally = Rally.objects.create(starts_on=now)

        new_starts_on = now + timedelta(hours=1)
        url = reverse('rally-update', kwargs={'id': rally.id})
        data = {'starts_on': new_starts_on}
        response = self.client.put(url, data, format='json')

        rally.refresh_from_db()
        rally_serializer = RallySerializer(rally)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, rally_serializer.data)
        self.assertEqual(rally.starts_on, new_starts_on)
