"""All Attendance API views."""
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from ..serializers.attendance import *
from ..models import Attendance, Event


class AttendanceCreateView(CreateAPIView):
    """Creates an Attendance."""
    queryset = Attendance.objects.all()
    serializer_class = AttendanceCreateSerializer


class AttendanceUpdateView(UpdateAPIView):
    """Updates an Attendance."""
    queryset = Attendance.objects.all()
    serializer_class = AttendanceUpdateSerializer


class AttendanceDashboardListView(ListAPIView):
    """Lists Attendances."""
    queryset = Attendance.objects.all()
    serializer_class = AttendanceDashboardListSerializer

    def get_queryset(self):
        event = Event.objects.get(
            pk=self.kwargs.get('event'))
        queryset = Attendance.objects.all().filter(event=event)
        return queryset
