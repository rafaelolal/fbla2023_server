from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Attendance, Event, Student, Prize
from ..serializers.student import (StudentCreateSerializer, StudentListSerializer,
                                   StudentLeaderboardListSerializer,
                                   StudentRetrieveSerializer, StudentEventListSerializer,
                                   StudentUpdateSerializer)

# class StudentTests(APITestCase):
#     def test_create_student(self):
#         url = reverse('student-create')
#         data = {'id': 'test_id', 'email': 'student_create@test.com'}
#         response = self.client.post(url, data)
#         student = Student.objects.get()
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Student.objects.count(), 1)
#         self.assertEqual(student.id, data['id'])
#         self.assertEqual(student.email, data['email'])

#     def test_list_student(self):
#         url = reverse('student-list')
#         Student.objects.create(id='test_id', email='student_list@test.com')
#         Student.objects.create(id='test_id2', email='student_list2@test.com')
#         response = self.client.get(url)
#         expected_data = student_serializers.StudentListSerializer(
#             Student.objects.all(), many=True).data
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), Student.objects.count())
#         self.assertEqual(response.data, expected_data)

#     def test_list_leaderboard_student(self):
#         url = reverse('student-leaderboard-list')
#         Student.objects.create(id='test_id', email='student_leaderboard_list@test.com',
#                                first_name='John', middle_name='Omar', last_name='Doe', points=100, rank=1)
#         Student.objects.create(id='test_id2', email='student_leaderboard_list2@test.com',
#                                first_name='Jane', middle_name='Holy', last_name='Dane', points=50, rank=2)
#         response = self.client.get(url)
#         expected_data = student_serializers.StudentLeaderboardListSerializer(
#             Student.objects.all(), many=True).data
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), Student.objects.count())
#         self.assertEqual(response.data, expected_data)

#     def test_retrieve_student(self):
#         student = Student.objects.create(id='test_id', email='student_retrieve@test.com',
#                                          first_name='John', middle_name='Omar', last_name='Doe', biography="I am John Omar Doe", grade=5, points=100, rank=1)
#         url = reverse('student-retrieve', args=[student.id])
#         event1 = Event.objects.create(title='Test Event', description='This is a test', type='Competition', location='Room 200',
#                                       starts_on=datetime.datetime.now(), finishes_on=datetime.datetime.now(), image='test_image.jpg', points=10)
#         event2 = Event.objects.create(title='Test Event 2', description='This is a test 2', type='Trip', location='Room 202',
#                                       starts_on=datetime.datetime.now(), finishes_on=datetime.datetime.now(), image='test_image.jpg', points=10)
#         student.events.add(
#             Attendance.objects.create(student=student, event=event1)
#         )
#         student.events.add(
#             Attendance.objects.create(student=student, event=event2)
#         )
#         response = self.client.get(url)
#         expected_data = student_serializers.StudentRetrieveSerializer(
#             student).data
#         response.data['image'] = response.data['image'].replace(
#             'http://testserver', '')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, expected_data)

#     def test_list_events_student(self):
#         student = Student.objects.create(
#             id='test_id', email='student_retrieve@test.com')
#         url = reverse('student-events-list', args=[student.id])
#         event1 = Event.objects.create(title='Test Event', description='This is a test', type='Competition', location='Room 200',
#                                       starts_on=datetime.datetime.now(), finishes_on=datetime.datetime.now(), image='test_image.jpg', points=10)
#         event2 = Event.objects.create(title='Test Event 2', description='This is a test 2', type='Trip', location='Room 202',
#                                       starts_on=datetime.datetime.now(), finishes_on=datetime.datetime.now(), image='test_image.jpg', points=10)
#         Student.objects.get().events.add(
#             Attendance.objects.create(student=student, event=event1)
#         )
#         Student.objects.get().events.add(
#             Attendance.objects.create(student=student, event=event2)
#         )
#         response = self.client.get(url)
#         expected_data = student_serializers.StudentRetrieveSerializer(
#             Student.objects.get()).data
#         response.data['image'] = response.data['image'].replace(
#             'http://testserver', '')
#         print(response.data, 'response')
#         print(expected_data, 'expected')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, expected_data)


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
            points=100,
            rank=1
        )

        url = reverse('student-leaderboard-list')
        serializer = StudentLeaderboardListSerializer([student], many=True)

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
        Prize.objects.create(student=student, type="Food")
        student.refresh_from_db()

        url = reverse('student-retrieve', kwargs={'pk': student.pk})
        serializer = StudentRetrieveSerializer(student)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_list_student_events(self):
        event1 = Event.objects.create(pk=100, title='Test Event', description='Test Description', type='Competition',
                                      location='Test Location', starts_on=datetime.now(tz=timezone.utc), finishes_on=datetime.now(tz=timezone.utc),
                                      points=10)
        event2 = Event.objects.create(pk=101, title='Test Event 2', description='Test Description', type='Competition',
                                      location='Test Location', starts_on=datetime.now(tz=timezone.utc), finishes_on=datetime.now(tz=timezone.utc),
                                      points=10)
        student = Student.objects.create(
            id='123',
            email='test@example.com',
            first_name='John',
            middle_name='Doe',
            last_name='Smith',
            grade=5
        )
        Attendance.objects.create(student=student, event=event1)
        Attendance.objects.create(student=student, event=event2)

        student.refresh_from_db()

        url = reverse('student-events-list', kwargs={'pk': student.pk})
        serializer = StudentEventListSerializer(student)

        response = self.client.get(url, format='json')

        print(response.data, "attendances data")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

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

        url = reverse('student-update', kwargs={'pk': student.pk})
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

        url = reverse('student-destroy', kwargs={'pk': student.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Student.objects.filter(pk=student.pk).exists())
