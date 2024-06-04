from django.test import TestCase, Client
from django.urls import reverse
from .models import TimeSlot, PoolOption, RoomOption, ServiceType, Service, Customer
from .forms import Frontpage
from datetime import datetime, timedelta

class FrontpageFormTest(TestCase):
    def test_form_validity(self):
        # Creating data for a valid form submission
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'service_type': ['pool', 'room'],
            'start_time': datetime.now(),
            'end_time': datetime.now() + timedelta(hours=2),
            'room_name': 'Conference',
            'room_attendees': 10,
            'room_special_orders': 'Extra chairs',
            'pool_name': 'Olympic',
            'pool_attendees': 15,
            'pool_special_orders': 'Extra lifeguard',
        }
        form = Frontpage(data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_if_end_time_before_start_time(self):
        data = {
            'start_time': datetime.now(),
            'end_time': datetime.now() - timedelta(hours=2),  # End time before start time
        }
        form = Frontpage(data)
        self.assertFalse(form.is_valid())
        self.assertIn('end_time', form.errors)  # Check that end_time is in the errors

class FrontpageViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.frontpage_url = reverse('frontpage')
        self.submitted_url = reverse('submitted')

    def test_frontpage_view_get(self):
        response = self.client.get(self.frontpage_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'frontpage.html')

    def test_frontpage_form_submission_redirects(self):
        # Assuming valid form data as used in the form test
        valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'service_type': ['pool', 'room'],
            'start_time': datetime.now(),
            'end_time': datetime.now() + timedelta(hours=2),
        }
        response = self.client.post(self.frontpage_url, valid_data)
        self.assertRedirects(response, self.submitted_url)

    def test_invalid_form_data_shows_errors(self):
        # Sending invalid data
        invalid_data = valid_data = {
            'start_time': datetime.now(),
            'end_time': datetime.now() - timedelta(hours=2),
        }
        response = self.client.post(self.frontpage_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'end_time', 'End time must be after start time.')

class SubmittedViewTest(TestCase):
    def test_submitted_view_get(self):
        response = self.client.get(reverse('submitted'))
        self.assertEqual(response.status_id_code, 200)
        self.assertTemplateUsed(response, 'submitted.html')
