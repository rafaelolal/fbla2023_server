"""All Prize serializers."""
from rest_framework import serializers
from ..models import Prize


class PrizeSerializer(serializers.ModelSerializer):
    """Used by Prize create and list view."""
    class Meta:
        model = Prize
        fields = ['name', 'type', 'cost']
