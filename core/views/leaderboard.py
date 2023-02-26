"""All Leaderboard API views."""
from datetime import date
from rest_framework.generics import UpdateAPIView
from ..serializers.leaderboard import *
from ..models import Leaderboard, Student


class LeaderboardUpdateView(UpdateAPIView):
    """Updates the Leaderboard creation date and recalculates students' ranks."""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardUpdateSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.created_on = date.today()
        instance.save()
        students = Student.objects.all().order_by('-live_points')
        for i, student in enumerate(students, 1):
            student.rank = i
            student.points = student.live_points
            student.save()

        response = super().put(request, *args, **kwargs)
        return response
