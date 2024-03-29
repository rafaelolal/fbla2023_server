"""All Student API views."""
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from ..serializers.student import *
from ..models import Student
from random import shuffle


class StudentCreateView(CreateAPIView):
    """Creates a Student."""
    queryset = Student.objects.all()
    serializer_class = StudentCreateSerializer


class StudentListView(ListAPIView):
    """Lists Students."""
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer

    def get_queryset(self):
        return Student.objects.all().order_by('last_name', 'first_name', 'middle_name')


class StudentRallyListView(ListAPIView):
    "Lists Students' names."

    queryset = Student.objects.all()
    serializer_class = StudentRallyListSerializer


class StudentLeaderboardListView(ListAPIView):
    """Lists Students for use in the leaderboard."""
    queryset = Student.objects.all()
    serializer_class = StudentLeaderboardListSerializer

    def get_queryset(self):
        return Student.objects.all().order_by('-current_points')


class StudentRetrieveView(RetrieveAPIView):
    """Retrieves a Student."""
    queryset = Student.objects.all()
    serializer_class = StudentRetrieveSerializer
    lookup_field = 'id'


class StudentEventListView(RetrieveAPIView):
    """Lists Student events."""
    queryset = Student.objects.all()
    serializer_class = StudentEventListSerializer
    lookup_field = 'id'


class StudentUpdateView(UpdateAPIView):
    """Updates a Student."""
    queryset = Student.objects.all()
    serializer_class = StudentUpdateSerializer
    lookup_field = 'id'


class StudentDestroyView(DestroyAPIView):
    """Destroys a Student."""
    queryset = Student.objects.all()
    serializer_class = StudentDestroySerializer
    lookup_field = 'id'
