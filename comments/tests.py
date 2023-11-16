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
        Comment.objects.create(
            post=self.post, owner=self.user, content="Test comment 1"
        )
        Comment.objects.create(
            post=self.post, owner=self.user, content="Test comment 2"
        )
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_user_can_retrieve_comment(self):
        comment = Comment.objects.create(
            post=self.post, owner=self.user, content='Test comment 1'
        )
        response = self.client.get(f'/comments/{comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Test comment 1')

    def test_logged_in_user_can_update_own_comment(self):
        self.client.login(username='testuser', password='test')
        comment = Comment.objects.create(
            post=self.post, owner=self.user, content='Original comment'
        )
        updated_data = {'content': 'Edited comment'}
        response = self.client.put(
            f'/comments/{comment.id}/', updated_data, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.get().content, 'Edited comment')

    def test_not_logged_in_user_cant_update_comment(self):
        self.comment = Comment.objects.create(
            owner=self.user, post=self.post, content='Test Comment'
        )
        self.comment_data = {'post': self.post.id, 'content': 'Edited comment'}
        urlpattern = f'/comments/{self.comment.id}/'
        response = self.client.put(urlpattern, self.comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_comment_owner_cant_update_comment(self):
        self.comment = Comment.objects.create(
            owner=self.user, post=self.post, content='Test comment'
        )
        other_user = User.objects.create_user(
            username='otheruser', password='test'
        )
        self.client.login(username='otheruser', password='test')
        urlpattern = f'/comments/{self.comment.id}/'
        response = self.client.put(urlpattern, self.comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_user_can_delete_comment(self):
        self.client.login(username='testuser', password='test')
        comment = Comment.objects.create(
            post=self.post, owner=self.user, content='Test comment'
        )
        response = self.client.delete(
            f'/comments/{comment.id}/', format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_not_logged_in_user_cant_delete_comment(self):
        comment = Comment.objects.create(
            post=self.post, owner=self.user, content='Test comment'
        )
        response = self.client.delete(
            f'/comments/{comment.id}/', format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_comment_owner_cant_delete_comment(self):
        self.comment = Comment.objects.create(
            owner=self.user, post=self.post, content='Test comment'
        )
        other_user = User.objects.create_user(
            username='otheruser', password='test'
        )
        self.client.login(username='otheruser', password='test')
        urlpattern = f'/comments/{self.comment.id}/'
        response = self.client.delete(urlpattern, self.comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)