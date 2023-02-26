from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from datetime import datetime, timedelta
from ..models import Student, Event, Attendance
from ..serializers.attendance import (
    AttendanceCreateSerializer,
    AttendanceUpdateSerializer,
    AttendanceDashboardListSerializer,
)


class AttendanceTestCase(APITestCase):
    def test_attendance_create(self):
        student = Student.objects.create(
            id='123',
            email='test@test.com',
            first_name='John',
            last_name='Doe',
            live_points=10,
            points=20,
            rank=1,
        )
        event = Event.objects.create(
            title='Test Event',
            description='This is a test event.',
            type='Competition',
            location='Test Location',
            starts_on=datetime.now(tz=timezone.utc),
            finishes_on=datetime.now(tz=timezone.utc) + timedelta(hours=1),
            points=10,
            is_canceled=False,
        )

        url = reverse('attendance-create')
        data = {'student': student.id, 'event': event.id}
        serializer = AttendanceCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, serializer.data)

    def test_attendance_update(self):
        student = Student.objects.create(
            id='123',
            email='test@test.com',
            first_name='John',
            last_name='Doe',
            live_points=10,
            points=20,
            rank=1,
        )
        event = Event.objects.create(
            title='Test Event',
            description='This is a test event.',
            type='Competition',
            location='Test Location',
            starts_on=datetime.now(tz=timezone.utc),
            finishes_on=datetime.now(tz=timezone.utc) + timedelta(hours=1),
            points=10,
            is_canceled=False,
        )
        attendance = Attendance.objects.create(student=student, event=event)

        url = reverse('attendance-update', kwargs={'pk': attendance.pk})
        data = {'attended': True}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        attendance.refresh_from_db()
        serializer = AttendanceUpdateSerializer(attendance)
        self.assertEqual(response.data, serializer.data)

    def test_attendance_dashboard_list(self):
        student = Student.objects.create(
            id='123',
            email='test@test.com',
            first_name='John',
            last_name='Doe',
            live_points=10,
            points=20,
            rank=1,
        )
        event = Event.objects.create(
            title='Test Event',
            description='This is a test event.',
            type='Competition',
            location='Test Location',
            starts_on=datetime.now(tz=timezone.utc),
            finishes_on=datetime.now(tz=timezone.utc) + timedelta(hours=1),
            points=10,
            is_canceled=False,
        )
        attendance = Attendance.objects.create(
            student=student, event=event)

        url = reverse('attendance-dashboard-list', kwargs={'event': event.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        attendance_list = Attendance.objects.filter(event=event)
        serializer = AttendanceDashboardListSerializer(
            attendance_list, many=True)
        self.assertEqual(response.data, serializer.data)
