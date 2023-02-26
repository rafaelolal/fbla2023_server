"""All Admin serializers."""
from rest_framework import serializers
from ..models import Admin


class AdminSerializer(serializers.ModelSerializer):
    """Used by Admin create and retrieve view."""
    class Meta:
        model = Admin
        fields = ['pk']
