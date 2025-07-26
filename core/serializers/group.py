"""All Group serializers."""
from rest_framework import serializers
from ..models import Group, GroupMember


class GroupSerializer(serializers.ModelSerializer):
    """Used by StudentRetrieve serializer and GraphQL."""
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'is_private', 'key']


class GroupMemberListSerializer(serializers.ModelSerializer):
    """Used by StudentRetrieve serializer and GraphQL."""
    group = GroupSerializer(read_only=True)

    class Meta:
        model = GroupMember
        fields = ['id', 'group']
