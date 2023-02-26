from datetime import datetime
from django.utils import timezone
from PIL import Image
from io import BytesIO
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Event
from ..serializers.event import (EventCreateSerializer, EventListSerializer,
                                 EventDashboardListSerializer, EventCancelUpdateSerializer)


class EventAPITestCase(APITestCase):

    def test_event_create(self):
        url = reverse('event-create')

        file = BytesIO()
        Image.new('RGB', (100, 100)).save(file, 'jpeg')
        file.name = 'test_image.jpg'
        file.seek(0)
        image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=file.read(),
            content_type='image/jpeg'
        )

        data = {'title': 'Test Event', 'description': 'Test Description', 'type': 'Competition',
                'location': 'Test Location', 'starts_on': datetime.now(tz=timezone.utc),
                'finishes_on': (datetime.now(tz=timezone.utc)), 'points': 10, 'image': image_file}

        serializer = EventCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        response = self.client.post(url, data, format='multipart')
        # response.data contains the URL while serializer.data contains None object
        # also, response.data contains is_canceled but serializer.data does not
        serializer_data = serializer.data.copy()
        del response.data['image']
        del serializer_data['image']
        del response.data['is_canceled']

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer_data)

    def test_event_list(self):
        url = reverse('event-list')
        Event.objects.create(title='Test Event', description='Test Description', type='Competition',
                             location='Test Location', starts_on=datetime.now(tz=timezone.utc), finishes_on=datetime.now(tz=timezone.utc),
                             points=10)
        serializer = EventListSerializer(Event.objects.all(), many=True)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_event_dashboard_list(self):
        url = reverse('event-dashboard-list')
        Event.objects.create(title='Test Event', description='Test Description', type='Competition',
                             location='Test Location', starts_on=datetime.now(tz=timezone.utc), finishes_on=datetime.now(tz=timezone.utc),
                             points=10)
        serializer = EventDashboardListSerializer(
            Event.objects.all(), many=True)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_event_cancel_update(self):
        event = Event.objects.create(title='Test Event', description='Test Description', type='Competition',
                                     location='Test Location', starts_on=datetime.now(tz=timezone.utc), finishes_on=datetime.now(tz=timezone.utc),
                                     points=10)
        url = reverse('event-cancel', kwargs={'pk': event.pk})
        data = {'cancellation_reason': 'Test reason'}

        serializer = EventCancelUpdateSerializer(instance=event, data=data)
        self.assertTrue(serializer.is_valid())

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_event_destroy(self):
        event = Event.objects.create(title='Test Event', description='Test Description', type='Competition',
                                     location='Test Location', starts_on=datetime.now(tz=timezone.utc), finishes_on=datetime.now(tz=timezone.utc),
                                     points=10)
        url = reverse('event-destroy', kwargs={'pk': event.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(pk=event.pk).exists())
