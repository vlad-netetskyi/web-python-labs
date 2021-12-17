import unittest

from flask_login import current_user
from flask import request
from flask_testing import TestCase

from app import bcrypt, db, create_app
from app.auth.models import User
import urllib


class BaseTestCase(TestCase):

    def create_app(self):
        self.baseURL = 'http://localhost:5000/'
        return create_app('test')

    def setUp(self):
        # self.client = self.app.test_client()
        db.create_all()
        db.session.add(User("admin", "admin.adm@in.com", "password"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_real_server_is_up_and_running(self):
        response = urllib.request.urlopen(self.baseURL)
        self.assertEqual(response.code, 200)

    def test_setup(self):
        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)


class FlaskTestCase(BaseTestCase):
    # Ensure that Flask was set up correctly
    def test_index(self):
        response = self.client.get('/auth/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that main page requires user login
    def test_main_route_requires_login(self):
        response = self.client.get('/auth/account', follow_redirects=True)
        self.assertIn(b'Remember me', response.data)


class UserViewsTests(BaseTestCase):

    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        response = self.client.get('/auth/login')
        self.assertIn(b'Remember me', response.data)

    # Ensure login behaves correctly with correct credentials
    def test_correct_register_and_login(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=dict(email="user.user@user.com",
                          username="user_name_",
                          password="password",
                          password_repeat="password"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn('Account created for', response.data)

            response = self.client.post(
                '/auth/login',
                data=dict(email="user.user@user.com", password="password"),
                follow_redirects=True
            )
            self.assertTrue(current_user.is_active)
            self.assert_200(response)

    def test_incorrect_login(self):
        response = self.client.post(
            '/auth/login',
            data=dict(email="wrong.email@email.ma", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid login!', response.data)


if __name__ == '__main__':
    unittest.main()
