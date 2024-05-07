from rest_framework.test import APITestCase
from rest_framework.serializers import ValidationError
from account.serializers.customer_serizliers import (
    RegisterCustomerSerializer,
    CustomerResetPasswordSerializer,
)


class TestRegisterCustomerSerializer(APITestCase):
    def test_password_match(self):
        data = {"email": "test@test.com", "password": "1", "password2": "1"}

        serializer = RegisterCustomerSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_password_not_match(self):
        data = {"email": "test@test.com", "password": "1", "password2": "2"}
        serializer = RegisterCustomerSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class TestCustomerResetPasswordSerializer(APITestCase):
    def test_password_match(self):
        data = {"new_password": 1, "new_password2": 1}
        serializer = CustomerResetPasswordSerializer(data=data)

        self.assertTrue(serializer.is_valid())

    def test_password_not_match(self):
        data = {"new_password": "1", "new_password2": "2"}
        serializer = CustomerResetPasswordSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
