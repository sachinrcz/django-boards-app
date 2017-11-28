from django.test import TestCase
from django.urls import reverse
from django.core.urlresolvers import resolve
from .views import home, board_topics, new_topic
from .models import Board, Topic, Post
from django.contrib.auth.models import User
from .forms import NewTopicForm
from accounts.views import signup
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
        self.assertEquals(views.func ,home)

    def test_board_links_in_home(self):
        board_topic_url = reverse('board_topics',kwargs={'pk':self.board.pk})
        self.assertContains(self.response,'href="{0}"'.format(board_topic_url))




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
        self.assertEquals(views.func, board_topics)

    def test_board_topic_contains_home_link(self):
        board_topics_url = reverse('board_topics',kwargs={'pk':self.board.pk })
        response = self.client.get(board_topics_url)
        home_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(home_url))


class NewTopicTests(TestCase):

    def setUp(self):
        self.board = Board.objects.create(name="Django",description="Test Description")
        User.objects.create_user(username='john')

    def test_csrf(self):
        url = reverse('new_topic',kwargs={'pk':1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'pk':1})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url,data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_new_topic_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_new_topic_success_code(self):
        url = reverse('new_topic', kwargs={'pk':self.board.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)

    def test_new_topic_not_found(self):
        url = reverse('new_topic', kwargs={'pk':99})
        response = self.client.get(url)
        self.assertEquals(response.status_code,404)

    def test_new_topic_resolve_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func,new_topic)

    def test_new_topic_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'pk':self.board.pk})
        board_topics_url = reverse('board_topics',kwargs={'pk':self.board.pk})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))


    def test_contains_form(self):
        url = reverse('new_topic',kwargs={'pk':self.board.pk})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form,NewTopicForm)


    def test_new_topic_invalid_data(self):
        url = reverse('new_topic',kwargs={'pk':self.board.pk})
        response = self.client.post(url,{})
        form = response.context.get('form')
        self.assertEquals(response.status_code,200)
        self.assertTrue(form.errors)


class signupTests(TestCase):

    def test_signup_status_code(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_signup_resolves_signup_views(self):
        view = resolve('/signup/')
        self.assertEquals(view.func,signup)
