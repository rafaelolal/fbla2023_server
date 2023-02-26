"""All Prize API views."""
from rest_framework.generics import ListAPIView, CreateAPIView
from ..serializers.prize import *
from ..models import Prize, Student


class PrizeCreateView(CreateAPIView):
    """Creates a Prize."""
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer


class PrizeListView(ListAPIView):
    """Lists Prizes."""
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer

    def get_queryset(self):
        student = Student.objects.get(
            pk=self.kwargs.get('student'))
        queryset = Prize.objects.all().filter(student=student)
        return queryset
