from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from model_bakery import baker

from account.models import User, CustomerProfile, DriverProfile
from trips.models import Comment, Trips


class TestCustomerCommentView(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse("trips:customer_comment")

        self.customer = User.objects.create_user(
            email="test@test.com", password="1", is_customer=True
        )
        self.customer_profile = CustomerProfile.objects.get(user=self.customer)
        self.customer_token = Token.objects.create(user=self.customer)

        self.customer2 = User.objects.create_user(
            email="test1@test.com", password="1", is_customer=True
        )
        customer_profile2 = CustomerProfile.objects.get(user=self.customer2)

        self.not_customer = User.objects.create_user(
            email="test2@test.com", password="1", is_customer=False
        )
        self.not_customer_token = Token.objects.create(user=self.not_customer)

        self.driver = User.objects.create_user(
            email="test3@test.com", password="1", is_driver=True
        )
        self.driver_profile = DriverProfile.objects.get(user=self.driver)

        self.trip = baker.make(
            Trips, customer=self.customer_profile, driver=self.driver_profile
        )

        self.comment = baker.make(Comment, customer=self.customer_profile, is_show=True)
        self.comment2 = baker.make(Comment, customer=customer_profile2, is_show=True)

    def test_get_customer_comments(self):
        response = self.client.get(
            self.url, headers={"Authorization": f"Token {self.customer_token.key}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_notcustomer_comment(self):
        response = self.client.get(
            self.url, headers={"Authorization": f"Token {self.not_customer_token.key}"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_customer_comment(self):
        data = {
            "customer": self.customer_profile.id,
            "driver": self.driver_profile.id,
            "trip": self.trip.id,
            "text": "test",
            "score ": 5,
        }
        response = self.client.post(
            self.url,
            data,
            headers={"Authorization": f"Token {self.customer_token.key}"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 3)

    def test_create_with_unvalid_data(self):
        data = {
            "customer": 1000,
            "driver": 1000,
            "trip": 1000,
            "text": "test" * 1000,
        }
        response = self.client.post(
            self.url,
            data,
            headers={"Authorization": f"Token {self.customer_token.key}"},
        )

        self.assertEqual(len(response.data.keys()), 4)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Comment.objects.count(), 2)


class TestCustomerCommentDetailView(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.customer = User.objects.create_user(
            email="test@test.com", password="1", is_customer=True
        )
        customer_profile = CustomerProfile.objects.get(user=self.customer)
        self.customer_token = Token.objects.create(user=self.customer)

        self.not_customer = User.objects.create_user(
            email="test2@test.com", password="1", is_customer=False
        )
        self.not_customer_token = Token.objects.create(user=self.not_customer)

        self.driver = User.objects.create_user(
            email="test3@test.com", password="1", is_driver=True
        )
        self.driver_profile = DriverProfile.objects.get(user=self.driver)

        self.trip = baker.make(
            Trips, customer=customer_profile, driver=self.driver_profile
        )

        self.comment = baker.make(Comment, customer=customer_profile, is_show=True)

    def test_get_detail_comment(self):
        url = reverse("trips:customer_comment_detail", kwargs={"id": self.comment.id})
        response = self.client.get(
            url,
            headers={"Authorization": f"Token {self.customer_token.key}"},
        )

        self.assertEqual(response.status_code, 200)
