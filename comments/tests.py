from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Comment
from posts.models import Post


class CommentViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='test'
            )

        self.post = Post.objects.create(
            title='Test Post', content='Test Content', owner=self.user
            )

        self.comment_data = {'post': self.post.id, 'content': 'Test Comment'}

    def test_logged_in_user_can_create_comment(self):
        self.client.login(username='testuser', password='test')
        response = self.client.post('/comments/', self.comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, 'Test Comment')

    def test_user_not_logged_in_cant_comment(self):
        response = self.client.post('/comments/', self.comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Comment.objects.count(), 0)

    def test_user_can_see_comment_list(self):
        