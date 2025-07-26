from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from ..models import Event, Student, Attendance
from ..serializers.event import (EventCreateSerializer, EventListSerializer,
                                 EventDashboardListSerializer, EventCancelUpdateSerializer)


class EventAPITestCase(APITestCase):

    def test_event_create(self):
        url = reverse('event-create')

        data = {'title': 'Test Event', 'description': 'Test Description', 'type': 'Competition',
                'location': 'Test Location', 'starts_on': datetime.now(tz=timezone.utc),
                'finishes_on': (datetime.now(tz=timezone.utc)), 'points': 10, 'image': "https://image_url.jpg"}

        serializer = EventCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        response = self.client.post(url, data, format='multipart')
        # response.data contains the URL while serializer.data contains None object
        serializer_data = serializer.data.copy()
        del response.data['image']
        del serializer_data['image']

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer_data)

    def test_event_list(self):
        url = reverse('event-list')
        Event.objects.create(title='Test Event 1', description='Test Description', type='Competition',
                             location='Test Location', starts_on=datetime.now(tz=timezone.utc) - timedelta(hours=1), finishes_on=datetime.now(tz=timezone.utc) - timedelta(hours=1),
                             points=10)
        Event.objects.create(title='Test Event 2', description='Test Description', type='Competition',
                             location='Test Location', starts_on=datetime.now(tz=timezone.utc) + timedelta(hours=1), finishes_on=datetime.now(tz=timezone.utc) + timedelta(hours=1),
                             points=10)
        Event.objects.create(title='Test Event 3', description='Test Description', type='Competition',
                             location='Test Location', starts_on=datetime.now(tz=timezone.utc) + timedelta(hours=2), finishes_on=datetime.now(tz=timezone.utc) + timedelta(hours=2),
                             points=10)
        serializer = EventListSerializer(Event.objects.all().filter(
            starts_on__gte=datetime.now(tz=timezone.utc)).order_by('starts_on'), many=True)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_event_dashboard_list(self):
        url = reverse('event-dashboard-list')
        student = Student.objects.create(id="test id", email="test@test.com")
        event = Event.objects.create(title='Test Event', description='Test Description', type='Competition',
                                     location='Test Location', starts_on=datetime.now(tz=timezone.utc), finishes_on=datetime.now(tz=timezone.utc),
                                     points=10)
        Attendance.objects.create(student=student, event=event)
        serializer = EventDashboardListSerializer(
            Event.objects.all(), many=True)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_event_cancel_update(self):
        event = Event.objects.create(title='Test Event', description='Test Description', type='Competition',
                                     location='Test Location', starts_on=datetime.now(tz=timezone.utc),
                                     finishes_on=datetime.now(tz=timezone.utc), points=10)
        url = reverse('event-cancel', kwargs={'id': event.id})
        data = {'cancelation_reason': 'Test reason'}
        serializer = EventCancelUpdateSerializer(instance=event, data=data)
        self.assertTrue(serializer.is_valid())
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_event_destroy(self):
        event = Event.objects.create(title='Test Event', description='Test Description', type='Competition',
                                     location='Test Location', starts_on=datetime.now(tz=timezone.utc), finishes_on=datetime.now(tz=timezone.utc),
                                     points=10)
        url = reverse('event-destroy', kwargs={'id': event.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=event.id).exists())
