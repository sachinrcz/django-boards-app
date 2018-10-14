from django.test import TestCase
from django.urls import reverse
from django.core.urlresolvers import resolve
from boards.views import board_topics, TopicListView
from boards.models import Board
# Create your tests here.



class BoardTopicTests(TestCase):

    def setUp(self):
        self.board = Board.objects.create(name="Test Board",description="Test Board Description")

    def test_board_view_status_code_success(self):
        url = reverse('board_topics', kwargs={'pk':self.board.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_view_status_code_error(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topic_url_resolves_board_topic_view(self):
        views = resolve('/boards/1/')
        self.assertEquals(views.func.view_class, TopicListView)

    def test_board_topic_contains_home_link(self):
        board_topics_url = reverse('board_topics',kwargs={'pk':self.board.pk })
        response = self.client.get(board_topics_url)
        home_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(home_url))

