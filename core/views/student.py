"""All Student API views."""
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from ..serializers.student import *
from ..models import Student


class StudentCreateView(CreateAPIView):
    """Creates a Student."""
    queryset = Student.objects.all()
    serializer_class = StudentCreateSerializer


class StudentListView(ListAPIView):
    """Lists Students."""
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer


class StudentLeaderboardListView(ListAPIView):
    """Lists Students for use in the leaderboard."""
    queryset = Student.objects.all()
    serializer_class = StudentLeaderboardListSerializer


class StudentRetrieveView(RetrieveAPIView):
    """Retrieves a Student."""
    queryset = Student.objects.all()
    serializer_class = StudentRetrieveSerializer


class StudentEventListView(RetrieveAPIView):
    """Lists Student events."""
    queryset = Student.objects.all()
    serializer_class = StudentEventListSerializer


class StudentUpdateView(UpdateAPIView):
    """Updates a Student."""
    queryset = Student.objects.all()
    serializer_class = StudentUpdateSerializer


class StudentDestroyView(DestroyAPIView):
    """Destroys a Student."""
    queryset = Student.objects.all()
    serializer_class = StudentDestroySerializer
