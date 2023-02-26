from .admin import AdminCreateView, AdminRetrieveView
from .attendance import AttendanceCreateView, AttendanceUpdateView, AttendanceDashboardListView
from .event import EventCreateView, EventListView, EventDestroyView, EventCancelUpdateView, EventDashboardListView
from .leaderboard import LeaderboardUpdateView
from .news import NewsListView, NewsCreateView, NewsDestroyView, NewsRetrieveView
from .prize import PrizeListView, PrizeCreateView
from .rally import RallyUpdateView
from .report import report_create_view, report_list_view, report_retrieve_view
from .student import StudentListView, StudentCreateView, StudentUpdateView, StudentDestroyView, StudentRetrieveView, StudentEventsListView, StudentLeaderboardListView
