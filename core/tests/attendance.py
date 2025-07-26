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
            balance=10,
            current_points=20,
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
        )

        url = reverse('attendance-create')
        data = {'student': student.id, 'event': event.id}
        serializer = AttendanceCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, serializer.data)

    def test_attendance_update(self):
        event = Event.objects.create(
            title='Test Event',
            description='This is a test event.',
            type='Competition',
            location='Test Location',
            starts_on=datetime.now(tz=timezone.utc),
            finishes_on=datetime.now(tz=timezone.utc) + timedelta(hours=1),
            points=10,
        )
        student1 = Student.objects.create(
            id='123',
            email='test@test.com',
        )
        student2 = Student.objects.create(
            id='1234',
            email='tes44t@test.com',
            balance=event.points
        )
        attendance1 = Attendance.objects.create(student=student1, event=event)
        attendance2 = Attendance.objects.create(
            student=student2, event=event, attended=True)

        url = reverse('attendance-update', kwargs={'id': attendance1.id})
        data = {'attended': True}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        attendance1.refresh_from_db()
        serializer = AttendanceUpdateSerializer(attendance1)
        self.assertEqual(response.data, serializer.data)
        student1.refresh_from_db()
        self.assertEqual(student1.balance, event.points)

        url = reverse('attendance-update', kwargs={'id': attendance2.id})
        data = {'attended': False}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        attendance2.refresh_from_db()
        serializer = AttendanceUpdateSerializer(attendance2)
        self.assertEqual(response.data, serializer.data)
        student2.refresh_from_db()
        self.assertEqual(student2.balance, 0)

    def test_attendance_dashboard_list(self):
        student = Student.objects.create(
            id='123',
            email='test@test.com',
            first_name='John',
            last_name='Doe',
            balance=10,
            current_points=20,
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
        )
        Attendance.objects.create(
            student=student, event=event)

        url = reverse('attendance-dashboard-list', kwargs={'event': event.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        attendance_list = Attendance.objects.filter(event=event)
        serializer = AttendanceDashboardListSerializer(
            attendance_list, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_attendance_destroy(self):
        student = Student.objects.create(id='test id', email="test@email.com")
        event = Event.objects.create(title='Test Event', description='Test Description', type='Competition',
                                     location='Test Location', starts_on=datetime.now(tz=timezone.utc), finishes_on=datetime.now(tz=timezone.utc),
                                     points=10)
        attendance = Attendance.objects.create(student=student, event=event)
        url = reverse('attendance-destroy', kwargs={'id': attendance.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Attendance.objects.filter(id=attendance.id).exists())
