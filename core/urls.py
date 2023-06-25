from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from .schema import schema


urlpatterns = [
    path('admin/create/', AdminCreateView.as_view(), name='admin-create'),
    path('admin/<str:id>/', AdminRetrieveView.as_view(), name='admin-retrieve'),

    path('attendance/create/', AttendanceCreateView.as_view(),
         name='attendance-create'),
    path('attendance/<int:id>/update/',
         AttendanceUpdateView.as_view(), name='attendance-update'),
    path('attendances/<int:event>/dashboard/',
         AttendanceDashboardListView.as_view(), name='attendance-dashboard-list'),
    path('attendance/<int:id>/destroy/',
         AttendanceDestroyView.as_view(), name='attendance-destroy'),

    path('event/create/', EventCreateView.as_view(), name='event-create'),
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/dashboard/', EventDashboardListView.as_view(),
         name='event-dashboard-list'),
    path('event/<int:id>/cancel/',
         EventCancelUpdateView.as_view(), name='event-cancel'),
    path('event/<int:id>/destroy/',
         EventDestroyView.as_view(), name='event-destroy'),

    path('leaderboard/<int:id>/update/',
         LeaderboardUpdateView.as_view(), name='leaderboard-update'),
    path('leaderboard/<int:id>/',
         LeaderboardRetrieveView.as_view(), name='leaderboard-retrieve'),

    path('news/create/', NewsCreateView.as_view(), name='news-create'),
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/<int:id>/', NewsRetrieveView.as_view(), name='news-retrieve'),
    path('news/<int:id>/destroy/', NewsDestroyView.as_view(), name='news-destroy'),

    path('prize/create/', PrizeCreateView.as_view(), name='prize-create'),
    path('prizes/<str:student>/', PrizeListView.as_view(), name='prize-list'),

    path('rally/<int:id>/', RallyRetrieveView.as_view(), name='rally-retrieve'),
    path('rally/<int:id>/update/', RallyUpdateView.as_view(), name='rally-update'),

    path('report/create/', report_create_view, name='report-create'),
    path('reports/', report_list_view, name='report-list'),
    path('report/<str:created_on>/', report_retrieve_view, name='report-retrieve'),

    path('student/create/', StudentCreateView.as_view(), name='student-create'),
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/leaderboard/', StudentLeaderboardListView.as_view(),
         name='student-leaderboard-list'),
    path('students/rally/', StudentRallyListView.as_view(),
         name='student-rally-list'),
    path('student/<str:id>/', StudentRetrieveView.as_view(),
         name='student-retrieve'),
    path('student/<str:id>/events/', StudentEventListView.as_view(),
         name='student-events-list'),
    path('student/<str:id>/update/',
         StudentUpdateView.as_view(), name='student-update'),
    path('student/<str:id>/destroy/',
         StudentDestroyView.as_view(), name='student-destroy'),
]

urlpatterns += [
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]
