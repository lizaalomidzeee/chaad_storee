from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from users.models import EmailVerificationCode
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from users.models import EmailVerificationCode



# User = get_user_model()

# class RegisterViewTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.register_url = reverse('register-list')
#         self.user_data = {
#             "username": "randomusername",
#             "email": "fake@gmail.com",
#             "password": "strongpassword123",
#             "password2": "strongpassword123",
#             "first_name": "nika",
#             "last_name": "nika",
#             "phone_number": "588585858"

#         }


#     def test_registration_success(self):
#         response = self.client.post(self.register_url, self.user_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())
#         user = User.objects.get(email=self.user_data['email'])
#         self.assertFalse(user.is_active)
#         self.assertTrue(EmailVerificationCode.objects.filter(user=user).exists())



#     def test_password_mismatch(self):
#         self.user_data['password2'] = 'newrandompassword123'
#         response = self.client.post(self.register_url, self.user_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('password', response.data)
#         self.assertFalse(User.objects.filter(email=self.user_data['email']).exists())




#     def test_user_registration_dublicate_email(self):
#         User.objects.create(
#             username = 'randomusername123',
#             email = self.user_data['email'],
#             password = 'randompassword123'
#         )

#         response = self.client.post(self.register_url, self.user_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('email', response.data)




class EmailVerificationnCodeTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(
            username = 'test123',
            email = 'test123@gmail.com',
            password = 'password123',
            is_active = False
        )

        self.confirm_url = reverse('register-confirm-code')
        self.verification_code = EmailVerificationCode.objects.create(
            user = self.user,
            code = '123456',
            created_at = timezone.now()
        )



    def test_successful_verification(self):
        data = {
            "email":"test123@gmail.com",
            "code":'123456'
        }
        response = self.client.post(self.confirm_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)



    def test_invalid_code(self):
        data = {
            "email" : "test123@gmail.com",
            "code": "712341"
        }
        response = self.client.post(self.confirm_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)



    def test_expired_code(self):
        self.verification_code.created_at = timezone.now() - timezone.timedelta(hours=24)
        self.verification_code.save()
        data = {
            "email" : "test123@gmail.com",
            "code" : "12345"
        }
        response = self.client.post(self.confirm_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
       


































# from django.core.cache import cache
# import random
# import time

# def expensive_calculations():
#     numbers = [i for i in range(10_000_000)]
#     random.shuffle(numbers)
#     numbers.sort()
#     return numbers


# def get_list():
#     start = time.time()
#     sorted_list = cache.get('numbers')
#     if not sorted_list:
#         sorted_list = expensive_calculations()
#         cache.set('numbers', sorted_list, 60 * 5)
#     end = time.time()
#     print(end-start)
#     return sorted_list

# get_list()
# get_list()
