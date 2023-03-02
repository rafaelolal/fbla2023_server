"""All Student serializers."""
from rest_framework import serializers
from ..models import Student
from ..serializers.attendance import AttendanceProfileListSerializer, AttendanceEventsListSerializer


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
        fields = ['email', 'first_name', 'middle_name',
                  'last_name', 'points', 'rank']


class StudentRetrieveSerializer(serializers.ModelSerializer):
    """Used by Student retrieve view."""
    events = AttendanceProfileListSerializer(many=True, read_only=True)
    prizes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = ['pk', 'first_name', 'middle_name', 'last_name',
                  'biography', 'grade', 'image', 'events', 'prizes']

    def get_prizes(self, obj):
        prizes = []
        for prize in obj.prizes.all():
            prizes.append(prize.type)
        return prizes


class StudentEventListSerializer(serializers.ModelSerializer):
    """Used by Student attendance list view."""
    attendances = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = ["attendances"]

    def get_attendances(self, obj):
        return obj.events.values('pk', 'event')


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
