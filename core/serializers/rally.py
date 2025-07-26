"""All Rally serializers."""
from rest_framework import serializers
from ..models import Rally


class RallySerializer(serializers.ModelSerializer):
    """Used by Rally create and list view."""
    class Meta:
        model = Rally
        fields = ['starts_on']
