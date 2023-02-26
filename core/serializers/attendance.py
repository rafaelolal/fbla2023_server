"""All Attendance serializers."""
from rest_framework import serializers
from ..models import Attendance


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


class AttendanceProfileListSerializer(serializers.ModelSerializer):
    """Used by Attendance profile list view."""
    class Meta:
        model = Attendance
        fields = ['event', 'attended']


class AttendanceDashboardListSerializer(serializers.ModelSerializer):
    """Used by Attendance dashboard list view."""
    class Meta:
        model = Attendance
        fields = ['pk', 'student', 'event', 'attended', 'final']
