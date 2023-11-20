from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import BookClubEvent
from responses.models import Response


class BookClubEventListViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='test'
        )
        self.other_user = User.objects.create_user(
            username='otheruser', password='othertest'
        )

        self.bookclubevent_data = {
            'event_name': 'Test Event',
            'event_description': 'Test Description',
            'owner': self.user
        }

    def test_user_logged_in_can_list_book_club_events(self):
        self.client.force_login(self.user)
        response = self.client.get('/bookclubevents/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_not_logged_in_can_list_book_club_events(self):
        response = self.client.get('/bookclubevents/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logged_in_can_retrieve_book_club_events(self):
        self.client.force_login(self.user)
        bookclubevent = BookClubEvent.objects.create(**self.bookclubevent_data)
        response = self.client.get(f'/bookclubevents/{bookclubevent.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['event_name'], 'Test Event')

    def test_user_not_logged_in_can_retrieve_book_club_events(self):
        bookclubevent = BookClubEvent.objects.create(**self.bookclubevent_data)
        response = self.client.get(f'/bookclubevents/{bookclubevent.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['event_name'], 'Test Event')

    def test_logged_in_user_can_create_a_book_club_event(self):
        self.client.force_login(self.user)
        user_id = self.user.id
        self.bookclubevent_data['owner'] = user_id
        response = self.client.post(
            '/bookclubevents/', self.bookclubevent_data, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookClubEvent.objects.count(), 1)
        self.assertEqual(BookClubEvent.objects.get().event_name, 'Test Event')

    def test_user_not_logged_in_cant_create_a_book_club_event(self):
        user_id = self.user.id
        self.bookclubevent_data['owner'] = user_id
        response = self.client.post(
            '/bookclubevents/', self.bookclubevent_data, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(BookClubEvent.objects.count(), 0)

class BookClubEventDetailViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='test'
        )
        self.other_user = User.objects.create_user(
            username='otheruser', password='othertest'
        )

        self.bookclubevent_data = {
            'event_name': 'Test Event',
            'event_description': 'Test Description',
            'owner': self.user
        }

    def test_user_logged_in_can_modify_own_book_club_event(self):
        bookclubevent = BookClubEvent.objects.create(**self.bookclubevent_data)
        self.client.force_login(self.user)
        response = self.client.put(
            f'/bookclubevents/{bookclubevent.id}/', {'event_name': 'Edited Event'}
            )
        bookclubevent.refresh_from_db()
        self.assertEqual(bookclubevent.event_name, 'Edited Event')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_not_logged_in_cant_modify_book_club_event(self):
        bookclubevent = BookClubEvent.objects.create(**self.bookclubevent_data)
        response = self.client.put(
            f'/bookclubevents/{bookclubevent.id}/', {'event_name': 'Edited Event'}
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_user_cant_modify_another_users_event(self):
        self.client.force_login(self.other_user)
        bookclubevent = BookClubEvent.objects.create(**self.bookclubevent_data)
        response = self.client.put(
            f'/bookclubevents/{bookclubevent.id}/',
            {'event_name': 'Edited Event by otheruser'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(bookclubevent.event_name, 'Test Event')

    def test_user_logged_in_can_delete_own_book_club_event(self):
        bookclubevent = BookClubEvent.objects.create(**self.bookclubevent_data)
        self.client.force_login(self.user)
        response = self.client.delete(
            f'/bookclubevents/{bookclubevent.id}/', {'event_name': 'Test Event'}
            )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_another_users_bookclubevent(self):
        bookclubevent = BookClubEvent.objects.create(**self.bookclubevent_data)
        self.client.force_login(self.other_user)
        response = self.client.delete(
            f'/bookclubevents/{bookclubevent.id}/', {'event_name': 'Test Event'}
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_not_logged_in_cant_delete_bookclubevent(self):
        bookclubevent = BookClubEvent.objects.create(**self.bookclubevent_data)
        response = self.client.delete(
            f'/bookclubevents/{bookclubevent.id}/', {'event_name': 'Test Event'}
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
