"""All Admin serializers."""
from rest_framework import serializers
from ..models import Admin, AdminAnnouncement


class AdminSerializer(serializers.ModelSerializer):
    """Used by Admin create and retrieve view."""
    class Meta:
        model = Admin
        fields = ['id']


class AdminAnnouncementSerializer(serializers.ModelSerializer):
    """Used by Admin create and retrieve view."""
    class Meta:
        model = AdminAnnouncement
        fields = ['id', 'title', 'content', 'created_on', 'expires_on']
