from django.test import TestCase
from rest_framework.test import APIClient
from event_management.models.event import Event
from event_management.models.attendee import Attendee
import pendulum
from django.urls import reverse

class AttendeeAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.event = Event.objects.create(
            name="Test Event",
            location="Test Location",
            start_time=pendulum.now('Asia/Kolkata').add(days=1),
            end_time=pendulum.now('Asia/Kolkata').add(days=1, hours=2),
            max_capacity=2,
            timezone="Asia/Kolkata"
        )
        self.attendee_data = {"name": "John Doe", "email": "john@example.com"}

    def test_register_attendee(self):
        response = self.client.post(reverse('register-attendee', kwargs={'event_id': str(self.event.id)}), self.attendee_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Attendee.objects.count(), 1)

    def test_prevent_duplicate_registration(self):
        self.client.post(reverse('register-attendee', kwargs={'event_id': str(self.event.id)}), self.attendee_data, format='json')
        response = self.client.post(reverse('register-attendee', kwargs={'event_id': str(self.event.id)}), self.attendee_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    def test_prevent_overbooking(self):
        self.client.post(reverse('register-attendee', kwargs={'event_id': str(self.event.id)}), self.attendee_data, format='json')
        self.client.post(reverse('register-attendee', kwargs={'event_id': str(self.event.id)}), {"name": "Jane Doe", "email": "jane@example.com"}, format='json')
        response = self.client.post(reverse('register-attendee', kwargs={'event_id': str(self.event.id)}), {"name": "Bob", "email": "bob@example.com"}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    def test_get_attendees(self):
        self.client.post(reverse('register-attendee', kwargs={'event_id': str(self.event.id)}), self.attendee_data, format='json')
        response = self.client.get(reverse('event-attendees', kwargs={'event_id': str(self.event.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)