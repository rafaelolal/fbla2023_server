"""All Attendance API views."""
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
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

    def patch(self, request, *args, **kwargs):
        object = Attendance.objects.get(pk=kwargs['pk'])
        response = super().patch(request, *args, **kwargs)
        request_attended = AttendanceUpdateSerializer(
            request.data).data['attended']
        if request_attended and not object.attended:
            object.student.live_points += object.event.points
            object.student.save()
        elif not request_attended and object.attended:
            object.student.live_points -= object.event.points
            object.student.save()
        return response


class AttendanceDashboardListView(ListAPIView):
    """Lists Attendances."""
    queryset = Attendance.objects.all()
    serializer_class = AttendanceDashboardListSerializer

    def get_queryset(self):
        event = Event.objects.get(
            pk=self.kwargs.get('event'))
        queryset = Attendance.objects.all().filter(event=event)
        return queryset


class AttendanceDestroyView(DestroyAPIView):
    """Destroy an Attendance."""
    queryset = Attendance.objects.all()
    serializer_class = AttendanceDestroySerializer
