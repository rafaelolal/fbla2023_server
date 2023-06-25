"""All Attendance serializers."""
from rest_framework import serializers
from ..models import Attendance, Event


class AttendanceCreateSerializer(serializers.ModelSerializer):
    """Used by Attendance create view."""
    class Meta:
        model = Attendance
        fields = ['student', 'event']


class AttendanceUpdateSerializer(serializers.ModelSerializer):
    """Used by Attendance update view."""
    class Meta:
        model = Attendance
        fields = ['attended']


class EventProfileSerializer(serializers.ModelSerializer):
    """Used by Attendance profile list serializer."""
    class Meta:
        model = Event
        fields = ['id', 'title', 'location', 'starts_on',
                  'finishes_on', 'cancelation_reason', 'type']


class AttendanceProfileListSerializer(serializers.ModelSerializer):
    """Used by Attendance profile list view."""
    event = EventProfileSerializer()

    class Meta:
        model = Attendance
        fields = ['event', 'attended']


class AttendanceEventsListSerializer(serializers.ModelSerializer):
    """Used by Student event list serializer."""
    class Meta:
        model = Attendance
        fields = ['event']


class AttendanceDashboardListSerializer(serializers.ModelSerializer):
    """Used by Attendance dashboard list view."""
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'event', 'attended',
                  'final', 'student_name']

    def get_student_name(self, obj):
        if all([obj.student.first_name, obj.student.middle_name, obj.student.last_name]):
            return f"{obj.student.first_name} {obj.student.middle_name} {obj.student.last_name}"
        else:
            return f"{obj.student.email}"


class AttendanceDestroySerializer(serializers.ModelSerializer):
    """Used by Attendance destroy view."""
    class Meta:
        model = Attendance
