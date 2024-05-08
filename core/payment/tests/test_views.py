import random
from datetime import timedelta
import stat

from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from model_bakery import baker

from account.models import User
from payment.models import Discount, DiscountUserProfile


class TestDiscountView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("payment:discount")
        self.passed_discount = baker.make(
            Discount, validate_time=timezone.now() - timedelta(days=1)
        )
        self.valid_discount = baker.make(
            Discount, validate_time=timezone.now() + timedelta(days=1)
        )
        self.superuser = User.objects.create_superuser(
            email="test@test.com",
            password="1",
        )
        self.token = Token.objects.create(user=self.superuser).key
        self.client = APIClient()

    def test_get_all_discount(self):
        response = self.client.get(
            self.url, headers={"Authorization": f"Token {self.token}"}
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 2)

    def test_create_discount(self):
        data = {
            "code": "test",
            "discount": random.randint(0, 100),
            "validate_time": timezone.now(),
        }
        response = self.client.post(
            self.url, data=data, headers={"Authorization": f"Token {self.token}"}
        )

        self.assertEqual(Discount.objects.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unvalid_data(self):
        data = {
            "code": "test",
            "discount": 101,
            "validate_time": "test",
        }
        response = self.client.post(
            self.url, data=data, headers={"Authorization": f"Token {self.token}"}
        )

        self.assertEqual(Discount.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data.keys()), 2)


class TestDeleteDiscountView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("payment:delete_discount")
        self.superuser = User.objects.create_superuser(
            email="test@test.com",
            password="1",
        )
        self.user = User.objects.create_user(
            email="test2@test.com",
            password="1",
        )
        self.user_token = Token.objects.create(user=self.user).key
        self.token = Token.objects.create(user=self.superuser).key
        self.client = APIClient()

    def test_delete_discount(self):
        discount = baker.make(Discount)
        discount_id = discount.id
        data = {"id": discount_id}
        response = self.client.delete(
            self.url, data=data, headers={"Authorization": f"Token {self.token}"}
        )

        self.assertFalse(Discount.objects.filter(id=discount_id).exists())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_superuser(self):
        discount = baker.make(Discount)
        discount_id = discount.id
        data = {"id": discount_id}
        response = self.client.delete(
            self.url, data=data, headers={"Authorization": f"Token {self.user_token}"}
        )

        self.assertTrue(Discount.objects.filter(id=discount_id).exists())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_not_valid_id(self):
        discount = baker.make(Discount)
        discount_id = discount.id
        data = {"id": 1000000}
        response = self.client.delete(
            self.url, data=data, headers={"Authorization": f"Token {self.token}"}
        )

        self.assertTrue(Discount.objects.filter(id=discount_id).exists())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDiscountDetailView(APITestCase):
    def setUp(self) -> None:
        self.customer = User.objects.create_user(
            email="test@test.com", password="1", is_customer=True
        )
        self.not_customer = User.objects.create_user(
            email="test2@test.com", password="2", is_customer=False
        )
        self.customer_token = Token.objects.create(user=self.customer).key
        self.not_customer_token = Token.objects.create(user=self.not_customer).key

        self.passed_discount = baker.make(
            Discount, validate_time=timezone.now() - timedelta(days=1)
        )
        self.valid_discount = baker.make(
            Discount, validate_time=timezone.now() + timedelta(days=1)
        )

        self.client = APIClient()

    def test_get_discount(self):
        url = reverse(
            "payment:discount_detail", kwargs={"code": self.valid_discount.code}
        )
        response = self.client.get(
            url, headers={"Authorization": f"Token {self.customer_token}"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.data,
            {
                "code": self.valid_discount.code,
                "discount": self.valid_discount.discount,
            },
        )

    def test_get_not_customer(self):
        url = reverse(
            "payment:discount_detail", kwargs={"code": self.valid_discount.code}
        )
        response = self.client.get(
            url, headers={"Authorization": f"Token {self.not_customer_token}"}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get("detail"), "You are not a valid customer!")

    def test_get_passed_code(self):
        url = reverse(
            "payment:discount_detail", kwargs={"code": self.passed_discount.code}
        )
        response = self.client.get(
            url, headers={"Authorization": f"Token {self.customer_token}"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("detail"), "discount code expired")

    def test_get_unvalid_code(self):
        url = reverse("payment:discount_detail", kwargs={"code": "test"})
        response = self.client.get(
            url, headers={"Authorization": f"Token {self.customer_token}"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get("detail"), "Not found.")