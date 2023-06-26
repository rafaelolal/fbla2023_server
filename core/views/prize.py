"""All Prize API views."""
from rest_framework.generics import ListAPIView, CreateAPIView
from ..serializers.prize import *
from ..models import Prize


class PrizeCreateView(CreateAPIView):
    """Creates a Prize."""
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer


class PrizeListView(ListAPIView):
    """Lists Prizes."""
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer
