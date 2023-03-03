"""All News serializers."""
from rest_framework import serializers
from ..models import News


class NewsCreateSerializer(serializers.ModelSerializer):
    """Used by News create view."""
    class Meta:
        model = News
        fields = ['title', 'content', 'created_on']


class NewsListSerializer(serializers.ModelSerializer):
    """Used by News list view."""
    class Meta:
        model = News
        fields = ['pk', 'title', 'created_on']


class NewsRetrieveSerializer(serializers.ModelSerializer):
    """Used by News retrieve view."""
    class Meta:
        model = News
        fields = ['title', 'content', 'created_on']


class NewsDestroySerializer(serializers.ModelSerializer):
    """Used by News destroy view."""
    class Meta:
        model = News
