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
            username='admin', password='admin', is_staff=True
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
        self.assertEqual(BookOfTheMonth.objects.count(), 1)

    def test_user_cant_create_book_of_the_month(self):
        self.client.force_login(self.user)
        response = self.client.post(
            '/bookofthemonth/', self.book_data, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_not_logged_in_can_retrieve_book_of_the_month(self):
        bookofthemonth = BookOfTheMonth.objects.create(**self.book_data)
        response = self.client.get(f'/bookofthemonth/{bookofthemonth.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Title')

    def test_user_logged_in_can_retrieve_book_of_the_month(self):
        self.client.force_login(self.user)
        bookofthemonth = BookOfTheMonth.objects.create(**self.book_data)
        response = self.client.get(f'/bookofthemonth/{bookofthemonth.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Title')

    def test_admin_can_edit_book_of_the_month(self):
        self.client.force_login(self.admin)
        bookofthemonth = BookOfTheMonth.objects.create(**self.book_data)
        edited_data = {
            'title': 'Edited Test Title',
            'content': 'Edited Test Content'
        }
        response = self.client.put(
            f'/bookofthemonth/{bookofthemonth.id}/', edited_data, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Edited Test Title')

    def test_user_cant_edit_book_of_the_month(self):
        self.client.force_login(self.user)
        bookofthemonth = BookOfTheMonth.objects.create(**self.book_data)
        edited_data = {
            'title': 'Edited Test Title',
            'content': 'Edited Test Content'
        }
        response = self.client.put(
            f'/bookofthemonth/{bookofthemonth.id}/', edited_data, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_book_of_the_month(self):
        self.client.force_login(self.admin)
        bookofthemonth = BookOfTheMonth.objects.create(**self.book_data)
        response = self.client.delete(f'/bookofthemonth/{bookofthemonth.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BookOfTheMonth.objects.count(), 0)

    def test_user_cant_delete_book_of_the_month(self):
        self.client.force_login(self.user)
        bookofthemonth = BookOfTheMonth.objects.create(**self.book_data)
        response = self.client.delete(f'/bookofthemonth/{bookofthemonth.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
