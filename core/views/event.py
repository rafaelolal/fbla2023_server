"""All Event API views."""
from datetime import datetime
from django.utils import timezone
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from ..serializers.event import *


class EventCreateView(CreateAPIView):
    """Creates an Event."""
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer


class EventListView(ListAPIView):
    """Lists Events."""
    queryset = Event.objects.all()
    serializer_class = EventListSerializer

    def get_queryset(self):
        queryset = Event.objects.all().filter(
            starts_on__gte=datetime.now(tz=timezone.utc)).order_by('starts_on')
        return queryset


class EventDashboardListView(ListAPIView):
    """Lists Events."""
    queryset = Event.objects.all()
    serializer_class = EventDashboardListSerializer

    def get_queryset(self):
        queryset = Event.objects.all().order_by('finishes_on')
        return queryset


class EventCancelUpdateView(UpdateAPIView):
    """Updates an Event for cancellation."""
    queryset = Event.objects.all()
    serializer_class = EventCancelUpdateSerializer


class EventDestroyView(DestroyAPIView):
    """Destroy an Event."""
    queryset = Event.objects.all()
    serializer_class = EventDestroySerializer
