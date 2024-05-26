from io import BytesIO
from rest_framework.test import APITestCase
from account.models import DriverProfile, User, CustomerProfile
from trips.models import DriverOffers, Trips
from rest_framework.authtoken.models import Token
from model_bakery import baker
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from trips.serializers.trips_serializers import (
    InputTripSerializer,
    DriverInputTripFinishSerializer,
)
from trips.views.trips_views import OrderTrips


class OrderTripsTest(APITestCase):

    def setUp(self):
        img = BytesIO(
            b"GIF89a\x01\x00\x01\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00"
            b"\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x01\x00\x00"
        )
        img.name = "myimage.jpg"

        self.user = User.objects.create_user(
            email="index@gmail.com", password="password123", is_customer=True,is_verified=True
        )
        self.user_profile = CustomerProfile.objects.get(user=self.user)
        self.user_profile.first_name = "index"
        self.user_profile.last_name = "uix"
        self.user_profile.cash_bank = 0
        self.user_profile.save()

        self.driver = User.objects.create_user(
            email="masoud@gmail.com",
            password="password123",
            is_driver=True,
        )

        self.profile = DriverProfile.objects.get(user=self.driver)
        self.profile.count_trip = 0
        self.profile.car = "SAMAND"
        self.profile.status = "No-travel"
        self.profile.image = img.name
        self.profile.save()

        self.token = Token.objects.create(user=self.user)
        self.driver_offer = baker.make(DriverOffers, driver=self.profile, active=True)
        self.driver_offer1 = baker.make(
            DriverOffers,
            driver=self.profile,
            active=True,
        )
        self.url = reverse("trips:orderoffer")

    def test_send_valid_data(self):
        headers = {"Authorization": f"Token {self.token.key}"}
        data = {"id": self.driver_offer.id}
        response = self.client.post(self.url, data=data, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(response.content,)
        # self.assertIn(self.driver_offer,response.data)
        self.assertEqual(
            response.data.get("driver"), self.driver_offer.driver.full_name
        )
        self.assertEqual(response.data.get("car"), self.driver_offer.driver.car)

    def test_unvalid_id(self):
        """
        this code have bug

        """

        headers = {"Authorization": f"Token {self.token.key}"}
        data = {"id": 1200}
        response = self.client.post(self.url, data=data, headers=headers)
        # print(response.content)
        serializer = InputTripSerializer(data=data)

        with self.assertRaises(ValidationError) as context:
            serializer.validate_id(data)

        self.assertIn("Your DriverOffer Dose Not Exists!", str(context.exception))

    def test_create_trips(self):
        OrderTrips.create_trips(offer=self.driver_offer, customer=self.user_profile)
        self.assertEqual(Trips.objects.count(), 1)

    def test_close_all_driver_offer(self):
        OrderTrips.close_all_driver_offer(driver=self.profile)
        self.driver_offer.refresh_from_db()
        self.driver_offer1.refresh_from_db()
        self.assertEqual(self.driver_offer.active, False)
        self.assertEqual(self.driver_offer1.active, False)

    def test_change_driver_status(self):

        OrderTrips.change_driver_status(driver=self.profile)
        self.driver_offer.refresh_from_db()
        self.driver_offer1.refresh_from_db()
        self.assertEqual(self.driver_offer.driver.status, "traveling")


class DriverTripsFinishTest(APITestCase):

    def setUp(self):

        # driver
        img = BytesIO(
            b"GIF89a\x01\x00\x01\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00"
            b"\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x01\x00\x00"
        )
        img.name = "myimage.jpg"

        self.driver = User.objects.create_user(
            email="masoud@gmail.com",
            password="password123",
            is_driver=True,
        )
        self.profile = DriverProfile.objects.get(user=self.driver)
        self.profile.count_trip = 0
        self.profile.car = "SAMAND"
        self.profile.status = "traveling"
        self.profile.image = img.name
        self.profile.save()

        self.user = User.objects.create_user(
            email="index@gmail.com", password="password123", is_customer=True,is_verified=True
        )
        self.user_profile = CustomerProfile.objects.get(user=self.user)
        self.user_profile.first_name = "index"
        self.user_profile.last_name = "uix"
        self.user_profile.cash_bank = 0
        self.user_profile.save()

        self.token = Token.objects.create(user=self.driver)

        self.driver_offer = baker.make(
            DriverOffers, driver=self.profile, active=True, end_key="12bi"
        )
        self.trips = baker.make(
            Trips,
            driver=self.profile,
            customer=self.user_profile,
            driver_offers=self.driver_offer,
        )
        self.url = reverse("trips:finishtrips")

    def test_unvalid_id(self):

        headers = {"Authorization": f"Token {self.token.key}"}
        data = {"id": 1200}
        self.client.patch(self.url, data=data, headers=headers)
        # print(response.content)
        serializer = DriverInputTripFinishSerializer(data=data)

        with self.assertRaises(ValidationError) as context:
            serializer.validate_id(data)

        self.assertIn("Your Trip do Not Exists!", str(context.exception))

    def test_unvalid_end_key(self):
        headers = {"Authorization": f"Token {self.token.key}"}
        data = {"id": self.trips.id, "end_key": "12dlf"}
        self.client.patch(self.url, data=data, headers=headers)

        serializer = DriverInputTripFinishSerializer(data=data)

        with self.assertRaises(ValidationError) as context:
            serializer.validate(data)

        self.assertIn("Your end_key wrong!", str(context.exception))

    def test_valid_data(self):
        headers = {"Authorization": f"Token {self.token.key}"}
        data = {"id": self.trips.id, "end_key": self.driver_offer.end_key}

        response = self.client.patch(self.url, data=data, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.profile.refresh_from_db()
        self.trips.refresh_from_db()
        self.assertEqual(self.profile.count_trip, 1)
        self.assertEqual(self.profile.status, "No-travel")
        self.assertTrue(self.trips.is_end)
