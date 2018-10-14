from django.test import TestCase
from django.urls import reverse
from django.core.urlresolvers import resolve
from boards.models import Board, Topic, Post
from django.contrib.auth.models import User
from ..views import topic_posts,TopicPostListView

class TopicPostTests(TestCase):

    def setUp(self):
        board  = Board.objects.create(name='Test Board',description= 'Just Another Test Board')
        user = User.objects.create(username='John',email='john@doe.com',password='1234')
        topic = Topic.objects.create(subject='Hello World',board=board,starter = user)
        post = Post.objects.create(message='Post Message',topic=topic,created_by=user)
        url = reverse('topic_posts',kwargs={'pk':board.pk,'topic_pk':topic.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_functions(self):
        view = resolve('/boards/1/topics/1/')
        self.assertEquals(view.func.view_class, TopicPostListView )