"""All Rally API views."""
from rest_framework.generics import UpdateAPIView
from ..serializers.rally import *
from ..models import Rally


class RallyUpdateView(UpdateAPIView):
    """Updates the Rally's start date and time."""
    queryset = Rally.objects.all()
    serializer_class = RallySerializer
