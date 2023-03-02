"""All Rally API views."""
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from ..serializers.rally import *
from ..models import Rally


class RallyRetrieveView(RetrieveAPIView):
    """Retrieves a Rally."""
    queryset = Rally.objects.all()
    serializer_class = RallySerializer


class RallyUpdateView(UpdateAPIView):
    """Updates the Rally's start date and time."""
    queryset = Rally.objects.all()
    serializer_class = RallySerializer
