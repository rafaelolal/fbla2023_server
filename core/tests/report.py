from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Report, Student, Event, Attendance, Leaderboard
from ..serializers.report import ReportSerializer


class ReportAPITestCase(APITestCase):
    def test_report_create_view(self):
        student = Student.objects.create(id='123', email='test@test.com', first_name='John',
                                         middle_name='Omar', last_name='Doe', grade=5,
                                         balance=100, current_points=200, rank=1)
        event = Event.objects.create(title='Test Event', description='Test description', type='Competition',
                                     location='Test location', starts_on='2023-02-25 08:00:00+00:00',
                                     finishes_on='2023-02-25 10:00:00+00:00', points=50)
        Attendance.objects.create(student=student, event=event)
        Leaderboard.objects.create()

        url = reverse('report-create')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        student.refresh_from_db()
        self.assertEqual(student.balance, 0)
        self.assertEqual(student.current_points, 0)
        self.assertIsNone(student.rank)

        attendance = Attendance.objects.get(student=student, event=event)
        self.assertTrue(attendance.final)

    def test_report_list_view(self):
        report1 = Report.objects.create(first_name='John', middle_name='M',
                                        last_name='Doe', points=100, grade=5)
        report2 = Report.objects.create(first_name='Jane', middle_name='A',
                                        last_name='Doe', points=200, grade=6)

        # the database automatically sets the date to today, so for testing purposes
        # I manually changed it
        report1.created_on = '2023-02-24'
        report2.created_on = '2023-02-25'
        report1.save()
        report2.save()

        url = reverse('report-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [{'created_on': '2023-02-25'},
                         {'created_on': '2023-02-24'}]

        self.assertEqual(response.data, expected_data)

    def test_report_retrieve_view(self):
        student1 = Student.objects.create(id='1245', email='test3@test.com', first_name='Jane',
                                          middle_name='M', last_name='Doe', biography='Test biography',
                                          grade=7, balance=4123, current_points=12311, rank=3)
        student2 = Student.objects.create(id='123', email='test1@test.com', first_name='John',
                                          middle_name='M', last_name='Doe', biography='Test biography',
                                          grade=5, balance=234, current_points=432, rank=1)
        student3 = Student.objects.create(id='1234', email='test2@test.com', first_name='Johnny',
                                          middle_name='M', last_name='Doe', biography='Test biography',
                                          grade=6, balance=2314, current_points=1234, rank=2)
        report1 = Report.objects.create(created_on='2023-02-25', first_name=student1.first_name, middle_name=student1.middle_name,
                                        last_name=student1.last_name, points=student1.balance, grade=student1.grade)
        report2 = Report.objects.create(created_on='2023-02-25', first_name=student2.first_name, middle_name=student2.middle_name,
                                        last_name=student2.last_name, points=student2.balance, grade=student2.grade)
        report3 = Report.objects.create(created_on='2023-02-25', first_name=student3.first_name, middle_name=student3.middle_name,
                                        last_name=student3.last_name, points=student3.balance, grade=student3.grade)

        # the database automatically sets the date to today, so for testing purposes
        # I manually changed it
        report1.created_on = '2023-02-25'
        report2.created_on = '2023-02-25'
        report3.created_on = '2023-02-25'
        report1.save()
        report2.save()
        report3.save()

        url = reverse('report-retrieve', kwargs={'created_on': '2023-02-25'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = ReportSerializer(Report.objects.all(), many=True).data
        self.assertEqual(response.data, expected_data)
