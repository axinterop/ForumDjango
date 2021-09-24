from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse


class PasswordResetMailTests(TestCase):
    def setUp(self):
        email_address = 'john@gmail.com'
        User.objects.create_user(username='john', email=email_address, password='abdcefg123456')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email_address})
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEquals('[Django Forum] Please reset your password', self.email.subject)

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid, 'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('john', self.email.body)
        self.assertIn('john@gmail.com', self.email.body)

    def test_email_to(self):
        self.assertEquals(['john@gmail.com'], self.email.to)
