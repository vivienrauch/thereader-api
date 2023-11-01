from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='testuser', password='test')

    def test_can_list_posts(self):
        testuser = User.objects.get(username='testuser')
        Post.objects.create(owner=testuser, title='test title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='testuser', password='test')
        response = self.client.post('/posts/', {'title': 'test title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'test title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailVewTests(APITestCase):
    def setUp(self):
        testuser1 = User.objects.create_user(
            username='testuser1', password='test1'
            )
        testuser2 = User.objects.create_user(
            username='testuser2', password='test2'
            )
        Post.objects.create(
            owner=testuser1, title='title1', content='test content 1'
        )
        Post.objects.create(
            owner=testuser2, title='title2', content='test content 2'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'title1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='testuser1', password='test1')
        response = self.client.put('/posts/1/', {'title': 'titleupdate'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'titleupdate')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_post(self):
        self.client.login(username='testuser1', password='test1')
        response = self.client.put('/posts/2/', {'title': 'titleupdate'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
