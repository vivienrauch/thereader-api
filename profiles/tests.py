from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Profile
from .serializers import ProfileSerializer


class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser1', password='testpass1'
        )
        self.profile_data = {
            'name': 'Hans Christian Andersen',
            'content': 'Test content',
            'fav_book': 'The Little Mermaid',
        }

    def test_create_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/profiles/', self.profile_data, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.get().owner, self.user)
