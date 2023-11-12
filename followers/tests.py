from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Follower


class FollowerListView(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1', password='test1'
            )
        self.user2 = User.objects.create_user(
            username='testuser2', password='test2'
        )

    """
    Test that logged in user can follow another user.
    """
    def test_user_logged_in_can_follow_another_user(self):
        self.client.login(username='testuser1', password='test1')
        urlpattern = '/followers/'
        data = {'followed': self.user2.id}
        response = self.client.post(urlpattern, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follower.objects.count(), 1)

    def test_user_not_logged_in_cant_follow_anyone(self):
        urlpattern = '/followers/'
        data = {'followed': self.user2.id}
        response = self.client.post(urlpattern, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Follower.objects.count(), 0)

    def test_user_logged_in_cant_follow_the_same_user_twice(self):
        self.client.login(username='testuser1', password='test1')
        urlpattern = '/followers/'
        data = {'followed': self.user2.id}
        response = self.client.post(urlpattern, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follower.objects.count(), 1)

        urlpattern_duplicate = '/followers/1'
        data = {'followed': self.user2.id}
        response_duplicate = self.client.post(
            urlpattern_duplicate, data, format='json'
            )
        self.assertEqual(
            response_duplicate.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
            )
        self.assertEqual(Follower.objects.count(), 1)