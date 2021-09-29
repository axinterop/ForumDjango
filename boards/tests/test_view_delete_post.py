from django.test import TestCase
from django.urls import reverse, resolve

from boards.models import Post, Topic, Board
from boards.models import User
from boards.views import PostDeleteView


class PostDeleteViewTestCase(TestCase):
    """
    Base test case to be used in all `PostDeleteView` view tests
    """

    def setUp(self):
        self.board = Board.objects.create(name='Python', description='Python board.')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.topic = Topic.objects.create(subject="Hello, world!", board=self.board, starter=user)
        self.post_initial = Post.objects.create(message="Initial post", topic=self.topic, created_by=user)
        self.post = Post.objects.create(message="Lorem ipsum dolor sit amet", topic=self.topic, created_by=user)
        self.url = reverse('delete_post', kwargs={
            'board_id': self.board.id, 'topic_id': self.topic.id, 'post_id': self.post.id
        })


class LoginRequiredPostDeleteViewTests(PostDeleteViewTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{}?next={}'.format(login_url, self.url))


class UnauthorizedPostDeleteViewTests(PostDeleteViewTestCase):
    def setUp(self):
        """
        Create a new user different from the one who posted
        """
        super().setUp()
        username = 'kevin'
        password = '321'
        user = User.objects.create_user(username=username, email='kevin@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        """
        A post should be delete only by the owner.
        Unauthorized users should get a 404 response (Page Not Found)
        """
        self.assertEquals(self.response.status_code, 404)


class PostDeleteViewTests(PostDeleteViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/boards/1/topics/1/posts/1/delete/')
        self.assertEquals(view.func.view_class, PostDeleteView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_confirm_btn(self):
        """
        The view must contain csrf and button
        """
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, 'name="delete_submit"', 1)  # <button name="delete_submit" ...


class SuccessfulPostDeleteTests(PostDeleteViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url)

    def test_redirection(self):
        """
        A valid post deletion should redirect the user to `topic_posts` view
        and show him the page where the post was deleted
        """
        topic_posts_url = reverse('topic_posts', kwargs={'board_id': self.board.id, 'topic_id': self.topic.id})
        url = '{url}?page={page}'.format(
            url=topic_posts_url,
            page=self.post.get_page(),
        )
        self.assertRedirects(self.response, url)

    def test_post_deleted(self):
        """
        After deleting the post, the total post count should be 1 (initial post remains)
        """
        self.assertEquals(Post.objects.count(), 1)


class InitialPostDeleteTestCase(PostDeleteViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        url_post_initial = reverse('delete_post', kwargs={
            'board_id': self.board.id, 'topic_id': self.topic.id, 'post_id': self.post_initial.id
        })
        self.response = self.client.post(url_post_initial)

    def test_redirection(self):
        """
        A valid initial post deletion should redirect the user to `board_topics` view
        """
        board_topics_url = reverse('board_topics', kwargs={'board_id': self.board.id})
        self.assertRedirects(self.response, board_topics_url)

    def test_topic_deleted(self):
        """
        After deleting the initial post, the total topic count should be 0
        """
        self.assertEquals(Topic.objects.count(), 0)

    def test_post_deleted(self):
        """
        After deleting the initial post, the total post count should be 0
        """
        self.assertEquals(Post.objects.count(), 0)
