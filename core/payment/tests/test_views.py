import random
from datetime import timedelta
import stat

from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from model_bakery import baker

from payment.views import VerifyPaid
from trips.models import Trips
from account.models import User , CustomerProfile
from payment.models import Discount, DiscountUserProfile,PayMentLog


class TestDiscountView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("payment:discount")
        cls.passed_discount = baker.make(
            Discount, validate_time=timezone.now() - timedelta(days=1)
        )
        cls.valid_discount = baker.make(
            Discount, validate_time=timezone.now() + timedelta(days=1)
        )
        cls.superuser = User.objects.create_superuser(
            email="test@test.com",
            password="1",
        )
        cls.token = Token.objects.create(user=cls.superuser).key
        cls.client = APIClient()

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
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("payment:delete_discount")
        cls.superuser = User.objects.create_superuser(
            email="test@test.com",
            password="1",
        )
        cls.user = User.objects.create_user(
            email="test2@test.com",
            password="1",
        )
        cls.user_token = Token.objects.create(user=cls.user).key
        cls.token = Token.objects.create(user=cls.superuser).key
        cls.client = APIClient()

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
    @classmethod
    def setUpTestData(cls):
        cls.customer = User.objects.create_user(
            email="test@test.com", password="1", is_customer=True,is_verified=True
        )
        cls.not_customer = User.objects.create_user(
            email="test2@test.com", password="2", is_customer=False
        )
        cls.customer_token = Token.objects.create(user=cls.customer).key
        cls.not_customer_token = Token.objects.create(user=cls.not_customer).key

        cls.passed_discount = baker.make(
            Discount, validate_time=timezone.now() - timedelta(days=1)
        )
        cls.valid_discount = baker.make(
            Discount, validate_time=timezone.now() + timedelta(days=1)
        )

        cls.client = APIClient()

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


class TestVerifyPaidView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@test.com',password="1",is_customer=True)
        cls.user2 = User.objects.create_user(email='test2@test.com',password="1",is_customer=True)
        
        cls.customer_profile = CustomerProfile.objects.get(user=cls.user)
        cls.customer_profile2 = CustomerProfile.objects.get(user=cls.user2)
        
        cls.trip1 = baker.make(Trips,customer=cls.customer_profile,is_paid=False,cost=100)
        cls.trip2 = baker.make(Trips,customer=cls.customer_profile,is_paid=False,cost=200)
        cls.trip3 = baker.make(Trips,customer=cls.customer_profile2,is_paid=False,cost=300)
        

    def test_create_payment_log(self):
        costs = self.trip1.cost + self.trip2.cost
        trips = Trips.objects.filter(customer=self.customer_profile)
        
        VerifyPaid.create_payment_log(user=self.user,trips=trips,cost=costs)
        
        self.assertEqual(PayMentLog.objects.count(),1)
        self.assertEqual(PayMentLog.objects.filter(user=self.user).count(),1)
        self.assertEqual(PayMentLog.objects.filter(user=self.user2).count(),0)
    
    
    def test_paid_trips(self):
        trips = Trips.objects.filter(customer=self.customer_profile)
        
        VerifyPaid.paid_trips(trips)
        
        self.trip1.refresh_from_db()
        self.trip2.refresh_from_db()
        self.trip3.refresh_from_db()
        
        self.assertTrue(self.trip1.is_paid)
        self.assertTrue(self.trip2.is_paid)
        self.assertFalse(self.trip3.is_paid)
        
        
        