"""All Leaderboard serializers."""
from rest_framework import serializers
from ..models import Leaderboard


class LeaderboardRetrieveSerializer(serializers.ModelSerializer):
    """Used by Leaderboard retrieve view."""
    class Meta:
        model = Leaderboard
        fields = ["created_on"]


class LeaderboardUpdateSerializer(serializers.ModelSerializer):
    """Used by Leaderboard update view."""
    class Meta:
        model = Leaderboard
        fields = []
