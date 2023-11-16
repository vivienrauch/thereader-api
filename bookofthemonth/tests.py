from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .models import BookOfTheMonth


class BookOfTheMonthViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='test'
        )
        self.admin = User.objects.create_user(
            username='admin', password='admin'
        )
        content_type = ContentType.objects.get_for_model(BookOfTheMonth)
        permission = Permission.objects.get(
            content_type=content_type, codename='view_bookofthemonth'
        )
        self.admin.user_permissions.add(permission)

        self.book_data = {
            'title': 'Test Title',
            'content': 'Test Content',
            'website': 'https://testsite.com'
        }

    def test_admin_can_create_book_of_the_month(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            '/bookofthemonth/', self.book_data, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)