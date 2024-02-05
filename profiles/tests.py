from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Profile


class ProfileListViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser1', password='testpass1'
        )
        self.profile_data = {
            'name': 'Hans Christian Andersen',
            'content': 'Test content',
            'fav_book': 'The Little Mermaid',
        }

    """
    Testing that both authenticated and not authenticated users
    can access the profile list.
    """
    def test_user_not_logged_in_can_list_profiles(self):
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logged_in_can_list_profiles(self):
        self.client.login(username='testuser', password='testpass1')
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_profile(self):
        """
        Testing that profile creation should not be accessible
        since it's handled by Django signals and not the view.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
                    '/profiles/',
                    self.profile_data,
                    format='json'
                    )
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
            )
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.get().owner, self.user)


class ProfileDetailViewTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1', password='testpass1'
        )
        self.user2 = User.objects.create_user(
            username='testuser2', password='testpass2'
        )

        self.profile_data1 = {
            'name': 'Hans Christian Andersen',
            'content': 'Test content',
            'fav_book': 'The Little Mermaid',
        }
        self.profile_data2 = {
            'name': 'George Orwell',
            'content': 'Test content2',
            'fav_book': '1984'
        }

    """
    Testing that both authenticated and not authenticated users
    can view profiles.
    """
    def test_user_logged_in_can_retrieve_profile(self):
        self.client.login(username='testuser1', password='testpass1')
        response = self.client.get('/profiles/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_not_logged_in_can_retrieve_profile(self):
        response = self.client.get('/profiles/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """
    Testing that only logged in users can update their own profile.
    """
    def test_user_not_logged_in_cant_update_profile(self):
        response = self.client.put('/profiles/1/', {'name': 'another name'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_logged_in_can_update_profile(self):
        self.client.login(username='testuser1', password='testpass1')
        response = self.client.put('/profiles/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_profile(self):
        self.client.login(username='testuser1', password='testpass1')
        response = self.client.put('/profiles/2/', {'name': 'another name'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    """
    Testing that a non-existent profile can't be retrieved.
    """
    def test_cant_retrieve_profile_using_invalid_id(self):
        response = self.client.get('/profiles/123/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
