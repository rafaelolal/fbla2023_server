"""All Event serializers."""
from rest_framework import serializers
from ..models import Event
from ..serializers.attendance import AttendanceDashboardListSerializer


class EventCreateSerializer(serializers.ModelSerializer):
    """Used by Event create view."""
    class Meta:
        model = Event
        fields = ['title', 'description', 'type', 'location', 'starts_on',
                  'finishes_on', 'image', 'points', 'cancelation_reason']


class EventListSerializer(serializers.ModelSerializer):
    """Used by Event list view."""
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'type', 'location', 'starts_on',
                  'finishes_on', 'image', 'points', 'cancelation_reason']


class EventDashboardListSerializer(serializers.ModelSerializer):
    """Used by Event dashboard list view."""
    participants = AttendanceDashboardListSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'type', 'location', 'starts_on',
                  'finishes_on', 'cancelation_reason', 'participants']


class EventProfileSerializer(serializers.ModelSerializer):
    """Used by Attendance profile list serializer."""
    class Meta:
        model = Event
        fields = ['id', 'title', 'location', 'starts_on',
                  'finishes_on', 'cancelation_reason']


class EventCancelUpdateSerializer(serializers.ModelSerializer):
    """Used by Event cancel update view."""
    class Meta:
        model = Event
        fields = ['cancelation_reason']


class EventDestroySerializer(serializers.ModelSerializer):
    """Used by Event destroy view."""
    class Meta:
        model = Event
