"""All Report serializers."""
from rest_framework import serializers
from ..models import Report


class ReportSerializer(serializers.ModelSerializer):
    """Used by all Report views."""
    class Meta:
        model = Report
        fields = ['created_on', 'first_name',
                  'middle_name', 'last_name', 'points', 'grade']


class ReportListSerializer(serializers.ModelSerializer):
    """Used by all Report views."""
    class Meta:
        model = Report
        fields = ['created_on']
