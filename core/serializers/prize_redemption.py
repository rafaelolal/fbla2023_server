"""All PrizeRedemption serializers."""
from rest_framework import serializers
from ..models import PrizeRedemption
# from .student import StudentRallyListSerializer
from .prize import PrizeSerializer


class PrizeRedemptionProfileListSerializer(serializers.ModelSerializer):
    """Used by StudentRetrieve serializer for own profile page"""
    prize = PrizeSerializer(read_only=True)

    class Meta:
        model = PrizeRedemption
        fields = ['prize', 'redeemed_on', 'approved_on']


# class PrizeRedemptionDashboardListSerializer(serializers.ModelSerializer):
#     """Used by [] [] for admin dashboard page"""
#     prize = PrizeSerializer(read_only=True)
#     student = StudentRallyListSerializer(read_only=True)

#     class Meta:
#         model = PrizeRedemption
#         fields = ['prize', 'student', 'redeemed_on', 'approved_on']
