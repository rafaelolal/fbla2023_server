"""All EventFeedback serializers."""
from rest_framework import serializers
from ..models import EventFeedback


class EventFeedbackSerializer(serializers.ModelSerializer):
    """Used by EventFeedback create mutation."""
    class Meta:
        model = EventFeedback
        fields = ['id', 'event', 'student', 'content',
                  'rating']
