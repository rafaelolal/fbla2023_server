"""All News API views."""
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from ..serializers.news import *
from ..models import News


class NewsCreateView(CreateAPIView):
    """Creates a News."""
    queryset = News.objects.all()
    serializer_class = NewsCreateSerializer


class NewsListView(ListAPIView):
    """Lists News."""
    queryset = News.objects.all()
    serializer_class = NewsListSerializer

    def get_queryset(self):
        return News.objects.all().order_by('-created_on')


class NewsRetrieveView(RetrieveAPIView):
    """Retrieves a News."""
    queryset = News.objects.all()
    serializer_class = NewsRetrieveSerializer


class NewsDestroyView(DestroyAPIView):
    """Destroys a News."""
    queryset = News.objects.all()
    serializer_class = NewsDestroySerializer
