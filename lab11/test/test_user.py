
# from . import BaseTestCase
# from flask_login import current_user
# from flask_testing import unittest


# # class UserViewsTests(BaseTestCase):

# #     # Ensure that the login page loads correctly
# #     def test_login_page_loads(self):
# #         response = self.client.get('/auth/login')
# #         print(response)
# #         self.assertIn(b'Please login', response.data)

# #     # Ensure login behaves correctly with correct credentials
# #     def test_correct_login(self):
# #         with self.client:
# #             response = self.client.post(
# #                 '/auth/login',
# #                 data=dict(email="admin.ad@min.com", password="admin"),
# #                 follow_redirects=True
# #             )
# #             self.assertIn(b'You are logged in', response.data)
# #             self.assertTrue(current_user.username == "admin")
# #             self.assertTrue(current_user.is_active())
# #             print(response)


# if __name__ == '__main__':
#     unittest.main()
