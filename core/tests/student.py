from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Attendance, Event, Student, Prize, PrizeRedemption, Group, GroupMember
from ..serializers.student import (StudentCreateSerializer, StudentListSerializer,
                                   StudentLeaderboardListSerializer,
                                   StudentRetrieveSerializer, StudentEventListSerializer,
                                   StudentRallyListSerializer)


class StudentTestCase(APITestCase):
    def test_create_student(self):
        url = reverse('student-create')
        data = {
            'id': '123',
            'email': 'test@example.com'
        }
        serializer = StudentCreateSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_list_students(self):
        student = Student.objects.create(
            id='123',
            email='test@example.com',
            first_name='John',
            middle_name='Doe',
            last_name='Smith',
            grade=5
        )

        url = reverse('student-list')
        serializer = StudentListSerializer([student], many=True)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_leaderboard_list_students(self):
        student = Student.objects.create(
            id='123',
            email='test@example.com',
            first_name='John',
            middle_name='Doe',
            last_name='Smith',
            current_points=100,
            rank=1
        )

        url = reverse('student-leaderboard-list')
        serializer = StudentLeaderboardListSerializer([student], many=True)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_rally_list_students(self):
        student = Student.objects.create(
            id='123',
            email='test@example.com',
            first_name='John',
            middle_name='Doe',
            last_name='Smith',
            grade=5
        )

        url = reverse('student-rally-list')
        serializer = StudentRallyListSerializer([student], many=True)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_student(self):
        event = Event.objects.create(title='Test Event 1', description='Test Description', type='Competition',
                                     location='Test Location', starts_on=datetime.now(tz=timezone.utc) - timedelta(hours=1), finishes_on=datetime.now(tz=timezone.utc) - timedelta(hours=1),
                                     points=10)
        student = Student.objects.create(
            id='123',
            email='test@example.com',
            first_name='John',
            middle_name='Doe',
            last_name='Smith',
            biography='Lorem ipsum',
            grade=5
        )
        Attendance.objects.create(student=student, event=event)
        prize = Prize.objects.create(name="Prize 1", type="Food", cost=10)
        PrizeRedemption.objects.create(
            prize=prize, student=student, redeemed_on=datetime.now(tz=timezone.utc), is_approved=False)
        group = Group.objects.create(
            name='Group Name', description='Group Description', is_private=True)
        GroupMember.objects.create(
            member=student, is_admin=True, group=group)

        student.refresh_from_db()

        url = reverse('student-retrieve', kwargs={'id': student.id})
        serializer = StudentRetrieveSerializer(student)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_list_student_events(self):
        event1 = Event.objects.create(id=100, title='Test Event', description='Test Description', type='Competition',
                                      location='Test Location', starts_on=datetime.now(tz=timezone.utc), finishes_on=datetime.now(tz=timezone.utc),
                                      points=10)
        event2 = Event.objects.create(id=101, title='Test Event 2', description='Test Description', type='Competition',
                                      location='Test Location', starts_on=datetime.now(tz=timezone.utc), finishes_on=datetime.now(tz=timezone.utc),
                                      points=10)
        student = Student.objects.create(
            id='123',
            email='test@example.com',
        )
        Attendance.objects.create(student=student, event=event1)
        Attendance.objects.create(student=student, event=event2)

        student.refresh_from_db()

        url = reverse('student-events-list', kwargs={'id': student.id})

        response = self.client.get(url, format='json')
        serializer = StudentEventListSerializer(student)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data),
                         str(serializer.data))

    def test_update_student(self):
        student = Student.objects.create(
            id='1234',
            email='test@example.com',
        )

        updated_data = {
            'first_name': 'Jane',
            'middle_name': 'A.',
            'last_name': 'Doe',
            'biography': 'Updated biography',
            'grade': 6,
            'image': 'https://image_url.jpg'
        }

        url = reverse('student-update', kwargs={'id': student.id})
        response = self.client.put(url, updated_data, format='multipart')

        # response.data contains the URL while updated_data contains the file object
        del response.data['image']
        del updated_data['image']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, updated_data)

    def test_destroy_student(self):
        student = Student.objects.create(
            id='1',
            email='testemail@example.com')

        url = reverse('student-destroy', kwargs={'id': student.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Student.objects.filter(id=student.id).exists())
