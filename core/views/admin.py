"""All Admin API views."""
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from ..serializers.admin import *
from ..models import Admin


class AdminCreateView(CreateAPIView):
    """Creates an Admin."""
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer


class AdminRetrieveView(RetrieveAPIView):
    """Retrieves an Admin."""
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    lookup_field = 'id'
