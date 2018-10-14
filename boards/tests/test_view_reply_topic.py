from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from ..models import Board,Topic,Post
from ..views import reply_topic
from ..forms import PostForm


class ReplyTopicTest(TestCase):

    def setUp(self):
        self.board = Board.objects.create(name="Test Board",description='Test Board Description')
        self.username = 'john'
        self.password = '1234'
        user = User.objects.create_user(username=self.username,email='john@doe.com',password=self.password)
        self.topic = Topic.objects.create(subject='Test Topic',board=self.board,starter=user)
        self.post = Post.objects.create(message='Test Message!',topic = self.topic,created_by=user)
        self.url = reverse('reply_topic',kwargs={'pk':self.board.pk,'topic_pk':self.topic.pk})


class LoginRequiredReplyTopicTests(ReplyTopicTest):


    def test_view_shows_login_page(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{}?next={}'.format(login_url,self.url))

class ReplyTopicTests(ReplyTopicTest):

    def setUp(self):
        super().setUp()
        self.client.login(username=self.username,password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_func(self):
        view_func = resolve('/boards/1/topics/1/reply/')
        self.assertEquals(view_func.func, reply_topic)

    def test_csrftoken(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form,PostForm)

        def test_form_inputs(self):
            '''
            The view must contain two inputs: csrf, message textarea
            '''
            self.assertContains(self.response, '<input', 1)
            self.assertContains(self.response, '<textarea', 1)

class SuccessfulReplyTopicTests(ReplyTopicTest):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'message': 'hello, world!'})

    def test_redirection(self):
        '''
        A valid form submission should redirect the user
        '''
        topic_posts_url = reverse('topic_posts', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})
        self.assertRedirects(self.response, topic_posts_url)

    def test_reply_created(self):
        '''
        The total post count should be 2
        The one created in the `ReplyTopicTestCase` setUp
        and another created by the post data in this class
        '''
        self.assertEquals(Post.objects.count(), 2)

class InvalidReplyTopicTests(ReplyTopicTest):
    def setUp(self):
        '''
        Submit an empty dictionary to the `reply_topic` view
        '''
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
