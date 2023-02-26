from django.urls import path
from .views import *

# path('event/<int:pk>/create', EventCreateView.as_view()),


urlpatterns = [
    path('admin/create/', AdminCreateView.as_view(), name='admin-create'),
    path('admin/<str:pk>/', AdminRetrieveView.as_view(), name='admin-retrieve'),

    path('attendance/create/', AttendanceCreateView.as_view(),
         name='attendance-create'),
    path('attendance/<int:pk>/update',
         AttendanceUpdateView.as_view(), name='attendance-update'),
    path('attendances/<int:event>/dashboard/',
         AttendanceDashboardListView.as_view(), name='attendance-dashboard-list'),

    path('event/create/', EventCreateView.as_view(), name='event-create'),
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/dashboard/', EventDashboardListView.as_view(),
         name='event-dashboard-list'),
    path('event/<int:pk>/cancel/',
         EventCancelUpdateView.as_view(), name='event-cancel'),
    path('event/<int:pk>/destroy/',
         EventDestroyView.as_view(), name='event-destroy'),

    path('leaderboard/<int:pk>/update/',
         LeaderboardUpdateView.as_view(), name='leaderboard-update'),

    path('news/create/', NewsCreateView.as_view(), name='news-create'),
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/<int:pk>/', NewsRetrieveView.as_view(), name='news-retrieve'),
    path('news/<int:pk>/destroy/', NewsDestroyView.as_view(), name='news-destroy'),

    path('prize/create/', PrizeCreateView.as_view(), name='prize-create'),
    path('prizes/<str:student>/', PrizeListView.as_view(), name='prize-list'),

    path('rally/<int:pk>/update/', RallyUpdateView.as_view(), name='rally-update'),

    path('report/create/', report_create_view, name='report-create'),
    path('reports', report_list_view, name='report-list'),
    path('report/<str:created_on>/', report_retrieve_view, name='report-retrieve'),

    path('student/create/', StudentCreateView.as_view(), name='student-create'),
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/leaderboard/', StudentLeaderboardListView.as_view(),
         name='student-leaderboard-list'),
    path('student/<str:pk>/', StudentRetrieveView.as_view(),
         name='student-retrieve'),
    path('student/<str:pk>/events/', StudentEventsListView.as_view(),
         name='student-events-list'),
    path('student/<str:pk>/update/',
         StudentUpdateView.as_view(), name='student-update'),
    path('student/<str:pk>/destroy/',
         StudentDestroyView.as_view(), name='student-destroy'),
]
