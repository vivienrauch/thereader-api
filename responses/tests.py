from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Response
from bookclubevents.models import BookClubEvent
from .serializers import ResponseSerializer


class ResponseListViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser1', password='testpass1'
        )
        self.bookclubevent = BookClubEvent.objects.create(
            event_name='Test Event',
            event_description='Test description',
            owner=self.user
        )

    """
    Test that both authenticated and not authenticated users can
    view response list.
    """
    def test_user_logged_in_can_view_responses(self):
        self.client.login(username='testuser1', password='testpass1')
        response = self.client.get('/responses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_not_logged_in_can_view_responses(self):
        response = self.client.get('/responses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    """
    Test that only logged in users can create a response.
    """
    def test_user_logged_in_can_create_response(self):
        self.client.force_authenticate(user=self.user)

        response_data = {
            'owner': self.user.id,
            'bookclubevent': self.bookclubevent.id
        }
        response = self.client.post(
            '/responses/',
            response_data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Response.objects.count(), 1)
        self.assertEqual(Response.objects.get().owner, self.user)

    def test_user_not_logged_in_cant_create_response(self):
        response_data = {
            'owner': self.user.id,
            'bookclubevent': self.bookclubevent.id
        }
        response = self.client.post(
            '/responses/',
            response_data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Response.objects.count(), 0)


class ResponseDetailViewTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1', password='testpass1'
        )
        self.user2 = User.objects.create_user(
            username='testuser2', password='testpass2'
        )
        self.bookclubevent1 = BookClubEvent.objects.create(
            event_name='Test Event',
            event_description='Test description',
            owner=self.user1,
        )
        self.bookclubevent2 = BookClubEvent.objects.create(
            event_name='Test Event2',
            event_description='Test description2',
            owner=self.user2
        )
        self.response1 = Response.objects.create(
            owner=self.user1,
            bookclubevent=self.bookclubevent1
        )
        self.response2 = Response.objects.create(
            owner=self.user2,
            bookclubevent=self.bookclubevent2
        )

    """
    Test that both authenticated an not authenticated users can
    retrieve individual responses.
    """
    def test_user_logged_in_can_retrieve_response(self):
        self.client.login(username='testuser1', password='testpass1')
        response = self.client.get('/responses/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_not_logged_in_can_retrieve_response(self):
        response = self.client.get('/responses/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """
    Test that users can't retrieve a response that doesn't exist.
    """
    def test_user_cant_retireve_non_existent_response(self):
        response = self.client.get('/responses/123/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    """
    Test that only logged in users can update only their own response.
    """
    def test_user_logged_in_cant_update_response(self):
        self.client.login(username='testuser1', password='testpass1')
        response = self.client.put('/responses/1/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_not_logged_in_cant_update_response(self):
        response = self.client.put('/responses/1/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_logged_in_can_delete_own_response(self):
        self.client.login(username='testuser1', password='testpass1')
        response = self.client.delete('/responses/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_logged_in_cant_delete_other_users_response(self):
        self.client.login(username='testuser1', password='testpass1')
        response = self.client.delete('/responses/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_not_logged_in_cant_delete_response(self):
        response = self.client.delete('/responses/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)