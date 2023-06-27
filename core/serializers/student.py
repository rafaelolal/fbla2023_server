"""All Student serializers."""
from rest_framework import serializers
from ..models import Student
from ..serializers.attendance import AttendanceProfileListSerializer, AttendanceEventsListSerializer
from ..serializers.group import GroupMemberListSerializer
from ..serializers.prize_redemption import PrizeRedemptionProfileListSerializer


class StudentCreateSerializer(serializers.ModelSerializer):
    """Used by Student create view."""
    class Meta:
        model = Student
        fields = ['id', 'email']


class StudentListSerializer(serializers.ModelSerializer):
    """Used by Student list view."""
    class Meta:
        model = Student
        fields = ['id', 'email', 'first_name',
                  'middle_name', 'last_name', 'grade']


class StudentLeaderboardListSerializer(serializers.ModelSerializer):
    """Used by Student leaderboard list view."""
    class Meta:
        model = Student
        fields = ['email', 'image', 'first_name', 'middle_name',
                  'last_name', 'current_points', 'rank']


class StudentRetrieveSerializer(serializers.ModelSerializer):
    """Used by Student retrieve view."""
    events = AttendanceProfileListSerializer(many=True, read_only=True)
    redemptions = PrizeRedemptionProfileListSerializer(
        many=True, read_only=True)
    groups = GroupMemberListSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'middle_name', 'last_name',
                  'biography', 'grade', 'image', 'events', 'redemptions',
                  'current_points', 'balance', 'rank', 'groups']


class StudentEventListSerializer(serializers.ModelSerializer):
    """Used by Student attendance list view."""
    attendances = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = ["attendances"]

    def get_attendances(self, obj):
        return obj.events.values('id', 'event')


class StudentRallyListSerializer(serializers.ModelSerializer):
    """Used by Student rally list view."""

    class Meta:
        model = Student
        fields = ['id', "first_name", 'last_name', 'middle_name']


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
