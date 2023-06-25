from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import News
from ..serializers.news import NewsCreateSerializer, NewsListSerializer, NewsRetrieveSerializer


class NewsAPITestCase(APITestCase):

    def test_create_news(self):
        url = reverse('news-create')
        data = {
            'title': 'Test News',
            'content': 'This is a test news',
        }
        serializer_data = NewsCreateSerializer(data=data)

        self.assertTrue(serializer_data.is_valid())

        response = self.client.post(url, data, format='json')
        # serializer_data does not return created_on
        del response.data['created_on']

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, serializer_data.validated_data)

    def test_list_news(self):
        url = reverse('news-list')
        news1 = News.objects.create(
            title='Test News 1', content='This is a test news 1')
        news2 = News.objects.create(
            title='Test News 2', content='This is a test news 2')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        serializer_data = NewsListSerializer([news1, news2], many=True)
        self.assertEqual(response.data, serializer_data.data)

    def test_retrieve_news(self):
        news = News.objects.create(
            title='Test News', content='This is a test news')
        url = reverse('news-retrieve', kwargs={'id': news.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        serializer_data = NewsRetrieveSerializer(news)
        self.assertEqual(response.data, serializer_data.data)

    def test_destroy_news(self):
        news = News.objects.create(
            title='Test News', content='This is a test news')
        url = reverse('news-destroy', kwargs={'id': news.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        self.assertFalse(News.objects.filter(id=news.id).exists())
