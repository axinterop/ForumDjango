from django.forms import ModelForm
from django.test import TestCase
from django.urls import reverse, resolve

from accounts.views import UserUpdateView
from boards.models import User


class UserUpdateViewTestCase(TestCase):
    """
    Base test case to be used in all `UserUpdateView` view tests
    """

    def setUp(self):
        self.username = 'john'
        self.password = '123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.url = reverse('my_account')


class LoginRequiredUserUpdateViewTests(UserUpdateViewTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{}?next={}'.format(login_url, self.url))


class UserUpdateViewTests(UserUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/settings/account/')
        self.assertEquals(view.func.view_class, UserUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        """
        The view must contain four inputs: csrf, email, first name and last name
        """
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="text"', 2)
        self.assertContains(self.response, 'type="email"', 1)


class SuccessfulUserUpdateTests(UserUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'email': 'anotheremail@gmail.com'})

    def test_redirection(self):
        """
        A valid form submission should redirect the user to `topic_posts` view
        """
        my_account_url = reverse('my_account')
        self.assertRedirects(self.response, my_account_url)

    def test_email_changed(self):
        self.user.refresh_from_db()
        self.assertEquals(self.user.email, 'anotheremail@gmail.com')


class InvalidUserUpdateTests(UserUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_not_valid_email_status_code(self):
        """
        An invalid form submission should return to the same page
        """
        self.assertEquals(self.response.status_code, 200)

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
