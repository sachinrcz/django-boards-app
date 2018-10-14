from django.test import TestCase
from django.urls import reverse
from django.core.urlresolvers import resolve
from boards.views import BoardListView
from boards.models import Board
# Create your tests here.


class HomeTest(TestCase):

    def setUp(self):
        self.board = Board.objects.create(name='Django',description='Django Desc')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code ,200)

    def test_home_url_resolve_to_home_view(self):
        views = resolve('/')
        self.assertEquals(views.func.view_class, BoardListView)

    def test_board_links_in_home(self):
        board_topic_url = reverse('board_topics',kwargs={'pk':self.board.pk})
        self.assertContains(self.response,'href="{0}"'.format(board_topic_url))

