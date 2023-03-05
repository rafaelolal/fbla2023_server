"""All Report API views."""
from datetime import date
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Report, Student, Attendance, Leaderboard
from ..serializers.report import ReportSerializer, ReportListSerializer


@api_view(['POST'])
def report_create_view(request):
    """Creates a Report, resets students' points and rank, and marks all attendances as final."""

    students = Student.objects.all()
    today = date.today()
    for student in students:
        report = Report(created_on=today, first_name=student.first_name or student.email, middle_name=student.middle_name,
                        last_name=student.last_name, points=student.live_points, grade=student.grade)
        report.save()
        student.live_points = 0
        student.points = 0
        student.rank = None
        student.save()

    leaderboard = Leaderboard.objects.get(pk=1)
    leaderboard.created_on = date.today()
    leaderboard.save()

    attendances = Attendance.objects.all().filter(final=False)
    for attendance in attendances:
        attendance.final = True
        attendance.save()

    return Response(data=ReportListSerializer(report).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def report_list_view(request):
    """Gets all the dates that Reports were created on."""

    created_ons = Report.objects.order_by(
        '-created_on').values('created_on').distinct()
    serializer = ReportListSerializer(created_ons, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def report_retrieve_view(request, created_on):
    """Lists all Report objects given a date."""

    reports = Report.objects.all().filter(
        created_on=created_on)
    serializer = ReportSerializer(reports, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
