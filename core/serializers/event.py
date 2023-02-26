"""All Event serializers."""
from rest_framework import serializers
from ..models import Event


class EventCreateSerializer(serializers.ModelSerializer):
    """Used by Event create view."""
    class Meta:
        model = Event
        fields = ['title', 'description', 'type', 'location', 'starts_on',
                  'finishes_on', 'image', 'points', 'is_canceled', 'cancellation_reason']


class EventListSerializer(serializers.ModelSerializer):
    """Used by Event list view."""
    class Meta:
        model = Event
        fields = ['pk', 'title', 'description', 'type', 'location', 'starts_on',
                  'finishes_on', 'image', 'points', 'is_canceled', 'cancellation_reason']


class EventDashboardListSerializer(serializers.ModelSerializer):
    """Used by Event dashboard list view."""
    class Meta:
        model = Event
        fields = ['pk', 'title', 'type', 'location', 'starts_on',
                  'finishes_on', 'is_canceled', 'cancellation_reason']


class EventCancelUpdateSerializer(serializers.ModelSerializer):
    """Used by Event cancel update view."""
    class Meta:
        model = Event
        fields = ['cancellation_reason']


class EventDestroySerializer(serializers.ModelSerializer):
    """Used by Event destroy view."""
    class Meta:
        model = Event
