import random
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase , APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from model_bakery import baker

from account.models import User  
from payment.models import Discount

class TestDiscountView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("payment:discount")
        self.passed_discount = baker.make(Discount,validate_time=timezone.now() - timedelta(days=1))
        self.valid_discount = baker.make(Discount,validate_time=timezone.now() + timedelta(days=1))
        self.superuser = User.objects.create_superuser(
            email="test@test.com", password="1",
        )
        self.token = Token.objects.create(user=self.superuser).key
        self.client = APIClient()

        
    
    def test_get_all_discount(self):
        response = self.client.get(self.url,headers={'Authorization' : f'Token {self.token}'})

        self.assertEquals(response.status_code,status.HTTP_200_OK)
        self.assertEquals(len(response.data),2)

    
    def test_create_discount(self):
        data = {
            'code':'test',
            'discount' : random.randint(0,100),
            'validate_time' : timezone.now(),
        }
        response = self.client.post(self.url,data=data,headers={'Authorization' : f'Token {self.token}'})
        
        self.assertEqual(Discount.objects.count(),3)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

class TestDeleteDiscountView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("payment:delete_discount")
        self.superuser = User.objects.create_superuser(
            email="test@test.com", password="1",
        )
        self.token = Token.objects.create(user=self.superuser).key
        self.client = APIClient()

    def test_delete_discount(self):
        discount = baker.make(Discount)
        discount_id = discount.id
        print(discount_id)
        data = {
            "id" : discount_id
        }
        response = self.client.delete(self.url,data=data,headers={'Authorization' : f'Token {self.token}'})

        self.assertFalse(Discount.objects.filter(id=discount_id).exists())
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

