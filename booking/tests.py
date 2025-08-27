from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from booking.models import TravelOption, Booking
from decimal import Decimal
import datetime
from django.utils import timezone


class TravelBookerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.travel = TravelOption.objects.create(
            type=TravelOption.TravelType.FLIGHT,
            source="Delhi",
            destination="Mumbai",
            departure=timezone.now() + datetime.timedelta(days=1),
            price=Decimal("5000.00"),
            available_seats=10,
        )

    def test_register_user(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
        })
        self.assertEqual(response.status_code, 302)  # should redirect
        self.assertTrue(User.objects.filter(username="newuser").exists())


    def test_login_logout_flow(self):
        # login
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "testpass123",
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("travel_list"))

        # logout
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("travel_list"))

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 302)  # redirect to login

        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)

    def test_travel_list_and_detail(self):
        response = self.client.get(reverse("travel_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delhi")

        response = self.client.get(reverse("travel_detail", args=[self.travel.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mumbai")

    def test_booking_creation_and_cancellation(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(reverse("book_now", args=[self.travel.id]), {
            "seats": 2
        })
        self.assertEqual(response.status_code, 302)
        booking = Booking.objects.filter(user=self.user, travel_option=self.travel).first()
        self.assertIsNotNone(booking)
        self.assertEqual(booking.number_of_seats, 2)
        response = self.client.post(reverse("cancel_booking", args=[booking.booking_id]))
        self.assertEqual(response.status_code, 302)
        booking.refresh_from_db()
        self.assertEqual(booking.status, Booking.Status.CANCELLED)
