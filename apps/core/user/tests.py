# from django.test import TestCase
# from user.models import User


# class UserCreationTest(TestCase):
#     def test_create_user(self):
#         email = 'testuser@example.com'
#         username = 'testuser'
#         first_name = 'Test'
#         password = 'testpassword'

#         user = User.objects.create_user(
#             email=email, username=username, first_name=first_name, password=password)
#         self.assertIsNotNone(user.pk)
#         self.assertEqual(user.email, email)
#         self.assertEqual(user.username, username)
#         self.assertTrue(user.check_password(password))
