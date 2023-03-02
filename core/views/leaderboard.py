"""All Leaderboard API views."""
from datetime import date
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from ..serializers.leaderboard import *
from ..models import Leaderboard, Student


class LeaderboardRetrieveView(RetrieveAPIView):
    """Retrieves a Leaderboard."""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardRetrieveSerializer


class LeaderboardUpdateView(UpdateAPIView):
    """Updates the Leaderboard creation date and recalculates students' ranks."""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardUpdateSerializer

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)

        students = Student.objects.all().order_by('-live_points')
        # removing student ranks to avoid unique constraint error
        for student in students:
            student.rank = None
            student.save()

        for i, student in enumerate(students, 1):
            student.rank = i
            student.points = student.live_points
            student.save()

        # cannot save in the above loop because
        # ranks must be unique

        return response
