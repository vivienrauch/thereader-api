from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Like
from posts.models import Post
from .serializers import LikeSerializer
from .views import LikeList, LikeDetail


class LikeListView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='test'
        )
        self.post = Post.objects.create(
            owner=self.user,
            title='Test post',
            content='Test content'
        )
        self.like_data = {
            'owner': self.user.id,
            'post': self.post.id
        }

    """
    Test that both authenticated and not authenticated users can view likes.
    """
    def test_user_logged_in_user_can_view_likes(self):
        self.client.login(username='testuser', password='test')
        response = self.client.get('/likes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_not_logged_in_user_can_view_likes(self):
        response = self.client.get('/likes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """
    Test that only logged in users can like posts.
    """
    def test_user_logged_in_can_like(self):
        self.client.login(username='testuser', password='test')
        response = self.client.post('/likes/1/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)