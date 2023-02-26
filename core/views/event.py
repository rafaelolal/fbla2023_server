"""All Event API views."""
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


class EventDashboardListView(ListAPIView):
    """Lists Events."""
    queryset = Event.objects.all()
    serializer_class = EventDashboardListSerializer


class EventCancelUpdateView(UpdateAPIView):
    """Updates an Event for cancellation."""
    queryset = Event.objects.all()
    serializer_class = EventCancelUpdateSerializer


class EventDestroyView(DestroyAPIView):
    """Destroy an Event."""
    queryset = Event.objects.all()
    serializer_class = EventDestroySerializer
