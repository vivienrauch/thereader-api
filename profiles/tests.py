from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Profile
from followers.models import Follower
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

    def test_listing_profiles(self):
        # Test listing profiles
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_profile(self):
        # Test creating profiles
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/profiles/', self.profile_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.get().owner, self.user)

    def test_authenticated_owner_can_retrieve_and_update_profile(self):
        self.client.force_authenticate(user=self.user)
        profile = Profile.objects.create(owner=self.user)
        response = self.client.get(f'/profiles/{profile.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_ok)
