"""All Leaderboard serializers."""
from rest_framework import serializers
from ..models import Leaderboard


class LeaderboardUpdateSerializer(serializers.ModelSerializer):
    """Used by Leaderboard update view."""
    class Meta:
        model = Leaderboard
        fields = []
