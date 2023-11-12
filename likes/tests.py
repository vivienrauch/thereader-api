from django.contrib.auth.models import User
from django.db.utils import IntegrityError
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
        response = self.client.post(
            '/likes/', self.like_data, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Like.objects.get().owner, self.user)
        self.assertEqual(Like.objects.get().post, self.post)

    def test_user_not_logged_in_cant_like(self):
        response = self.client.post(
            '/likes/', self.like_data, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Like.objects.count(), 0)


class LikeDetailView(APITestCase):
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
    Test that user can't like a post twice.
    """
    def test_user_cant_like_twice(self):
        self.client.login(username='testuser', password='test')
        response = self.client.post('/likes/', self.like_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response_duplicate = self.client.post('/likes/1/', self.like_data, format='json')
        self.assertEqual(response_duplicate.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Like.objects.count(), 1)

    """
    Test that logged in user can delete their own like.
    """
    def test_user_logged_in_can_delete_own_like(self):
        self.client.login(username='testuser', password='test')
        response_like = self.client.post('/likes/', self.like_data, format='json')
        self.assertEqual(response_like.status_code, status.HTTP_201_CREATED)
        response_delete_like = self.client.delete('/likes/1/', self.like_data, format='json')
        self.assertEqual(response_delete_like.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 0)

    """
    Test that a user can't unlike a post they didn't like.
    """
    def test_user_logged_in_cant_delete_other_users_like(self):
        self.client.login(username='testuser', password='test')
        response_delete_like = self.client.delete('/likes/1/', self.like_data, format='json')
        self.assertEqual(response_delete_like.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Like.objects.count(), 0)