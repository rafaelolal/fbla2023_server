"""All Student serializers."""
from rest_framework import serializers
from ..models import Student
from ..serializers.attendance import AttendanceProfileListSerializer


class StudentCreateSerializer(serializers.ModelSerializer):
    """Used by Student create view."""
    class Meta:
        model = Student
        fields = ['id', 'email']


class StudentListSerializer(serializers.ModelSerializer):
    """Used by Student list view."""
    class Meta:
        model = Student
        fields = ['pk', 'email', 'first_name',
                  'middle_name', 'last_name', 'grade']


class StudentLeaderboardListSerializer(serializers.ModelSerializer):
    """Used by Student leaderboard list view."""
    class Meta:
        model = Student
        fields = ['first_name', 'middle_name',
                  'last_name', 'points', 'rank']


class StudentRetrieveSerializer(serializers.ModelSerializer):
    """Used by Student retrieve view."""
    events = AttendanceProfileListSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['pk', 'first_name', 'middle_name', 'last_name',
                  'biography', 'grade', 'image', 'events']


class StudentEventListSerializer(serializers.ModelSerializer):
    """Used by Student events list view."""
    events = AttendanceProfileListSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ["events"]


class StudentUpdateSerializer(serializers.ModelSerializer):
    """Used by Student update view."""
    class Meta:
        model = Student
        fields = ['first_name', 'middle_name',
                  'last_name', 'biography', 'grade', 'image']


class StudentDestroySerializer(serializers.ModelSerializer):
    """Used by Student destroy view."""
    class Meta:
        model = Student
