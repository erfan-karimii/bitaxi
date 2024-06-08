from io import BytesIO
from django.test import TestCase
from account.models import User, DriverProfile
from django.test.client import RequestFactory
from account.permissions import IsDriver
from account.views.driver_views import DriverProfileView
from django.urls import reverse
from account.serializers.driver_serializers import (
    InputRegisterSerializers,
    DriverProfileSerializers,
)
from rest_framework.validators import ValidationError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, force_authenticate
from model_bakery import baker

# Permission


class IsDriverPermissionTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.user1 = User.objects.create_user(
            email="idnex@gmail.com", password="12", is_driver=True
        )
        cls.user2 = User.objects.create_user(
            email="test@gmail.com", password="12", is_customer=True
        )
        cls.view = DriverProfileView.as_view()
        cls.permission = IsDriver()

    def test_driver_permission(self):
        urls = self.factory.get(reverse("account:driverprofile"))
        urls.user = self.user1

        self.assertTrue(self.permission.has_permission(urls, self.view))

    def test_no_driver(self):
        urls = self.factory.get(reverse("account:driverprofile"))
        urls.user = self.user2
        self.assertFalse(self.permission.has_permission(urls, self.view))


# ------------------------- Serializers ------------------------------


class InputRegisterSerializersTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_data = {
            "email": "admin@admin.com",
            "password": "12",
            "password1": "12",
        }
        cls.invalid_data = {"email": "", "password": "12", "password1": "12"}

    def test_valid_data(self):
        serializer = InputRegisterSerializers(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        serializer = InputRegisterSerializers(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_password_not_same(self):
        data = {"email": "admin@admin.com", "password": "12", "password1": "3"}
        serializers = InputRegisterSerializers()

        with self.assertRaises(ValidationError) as context:
            serializers.validate(data)
        self.assertIn("Passowrd Does not same", str(context.exception.detail))

    def test_password_same(self):
        data = {"email": "admin@admin.com", "password": "12", "password1": "12"}
        serializer = InputRegisterSerializers()
        self.assertEqual(serializer.validate(attrs=data), data)


class DriverProfileSerializersTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="index@gmail.com", password="password123@", is_driver=True
        )
        cls.token = Token.objects.create(user=cls.user)
        cls.profile = DriverProfile.objects.get(user=cls.user)
        cls.url = reverse("account:driverprofile")
        cls.headers = {"Authorization": f"Token {cls.token.key}"}

    def test_get_email(self):
        cl_obj = DriverProfileSerializers()
        self.assertEqual(cl_obj.get_email(obj=self.profile), "index@gmail.com")

    def test_update_profile(self):
        img = BytesIO(
            b"GIF89a\x01\x00\x01\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00"
            b"\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x01\x00\x00"
        )
        img.name = "myimage.jpg"
        data = {
            "first_name": "Masoud",
            "last_name": "kheradmandi",
            "image": img,
            "cash_bank": 12,
            "car": "SAMAND",
            "count_trip": 12,
        }
        self.client.put(self.url, data=data, headers=self.headers)
        self.profile.refresh_from_db()

        self.assertEqual(self.profile.first_name, "Masoud")
        self.assertEqual(self.profile.last_name, "kheradmandi")
        self.assertEqual(self.profile.image, img)
        self.assertEqual(self.profile.cash_bank, 12)
        self.assertEqual(self.profile.car, "SAMAND")
        self.assertEqual(self.profile.count_trip, 0)


# ------------------------- Serializers ------------------------------


# --------------------------Views --------------------------------------


class TestDriverSignUp(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_data = {
            "email": "admin@admin.com",
            "password": "12",
            "password1": "12",
        }
        cls.un_valid = {
            "email": "admin@admin.com",
            "password": "122",
            "password1": "12",
        }
        cls.url = reverse("account:DriverSignUP")

    def test_valid_driver_signup(self):

        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data["email"], "admin@admin.com")
        self.assertEqual(
            response.data,
            {"email": "admin@admin.com", "message": "اکانت شما با موفقیت ساخته شد"},
        )

    def test_unvalid_driver_signup(self):

        response = self.client.post(self.url, data=self.un_valid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDriverSignIn(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            email="index@gmail.com", password="password123", is_driver=True
        )
        User.objects.create_user(
            email="customer@gmail.com", password="password123", is_driver=False
        )
        cls.url = reverse("account:DriverSignIn")

    def test_valid_login(self):
        data = {"email": "index@gmail.com", "password": "password123"}
        response = self.client.post(self.url, data=data)
        # self.assertEqual(response)
        self.assertEqual(response.data["email"], "index@gmail.com")

    def test_unvalid_login_user_does_not_exists(self):
        unvalid_data = {"email": "tset@gmail.com", "password": "password123"}
        response = self.client.post(self.url, data=unvalid_data)
        self.assertIn(
            "Unable to log in with provided credentials.", str(response._container)
        )

    def test_unvalid_login_user_not_driver(self):
        unvalid_data = {"email": "customer@gmail.com", "password": "password123"}
        response = self.client.post(self.url, data=unvalid_data)
        self.assertIn("You are Not Driver!", str(response.content))


class ResetPasswordTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="index@gmail.com", password="password123@", is_driver=True
        )
        cls.token = Token.objects.create(user=cls.user)
        cls.url = reverse("account:reset_password")

    def test_valid_reset_password(self):
        data = {"new_password": "password1234", "new_password1": "password1234"}

        headers = {"Authorization": f"Token {self.token.key}"}
        response = self.client.put(self.url, data=data, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertIn("Your Password Changed", response.content.decode("utf-8"))

    def test_unvalid_reset_password(self):
        data = {"new_password": "password34", "new_password1": "password1234"}
        headers = {"Authorization": f"Token {self.token.key}"}

        response = self.client.put(path=self.url, data=data, headers=headers)
        self.assertIn("Passowrd Does not same", response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ForgetPasswordTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="index@gmail.com", password="password123@", is_driver=True
        )
        cls.url = reverse("account:forget_password")

    def test_valid_data(self):
        data = {"email": "index@gmail.com"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(data["email"], str(response.content))

    def test_unvalid_data(self):
        data = {"email": 12}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Enter valid email", str(response.content))

    def test_unvalid_data_email_does_not_exists(self):
        data = {"email": "masoud@gamil.com"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Email Does Not exist", str(response.content))


class VerifyForgetPasswordTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="index@gmail.com", password="password123@", is_driver=True
        )
        cls.token = Token.objects.create(user=cls.user)

    def test_valid_token(self):
        url = reverse("account:vrify", args=[self.token.key])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["token"], self.token.key)
        self.assertEqual(response.data["msg"], "success fully return")

    def test_unvalid_token(self):
        bad_token = "1faac6261e834d406fe84d3b3561413fc579d2a5"
        url = reverse("account:vrify", args=[bad_token])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["msg"], "time error")


class DriverProfileViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="index@gmail.com", password="password123@", is_driver=True
        )
        cls.token = Token.objects.create(user=cls.user)
        cls.profile = DriverProfile.objects.get(user=cls.user)
        cls.url = reverse("account:driverprofile")
        cls.headers = {"Authorization": f"Token {cls.token.key}"}

    def test_show_profile(self):
        response = self.client.get(self.url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "index@gmail.com")

    def test_update_profile(self):
        img = BytesIO(
            b"GIF89a\x01\x00\x01\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00"
            b"\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x01\x00\x00"
        )
        img.name = "myimage.jpg"
        data = {
            "first_name": "Masoud",
            "last_name": "kheradmandi",
            "image": img,
            "cash_bank": 12,
            "car": "SAMAND",
            "count_trip": 12,
        }
        response = self.client.put(self.url, data=data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn("your update success", str(response.content))

    def test_update_by_unvalid_data(self):
        bad_data = {
            "first_name": "Masoud",
            "last_name": "kheradmandi",
            "cash_bank": 12,
            "car": "SAMAND",
            "count_trip": 12,
        }
        response = self.client.put(self.url, data=bad_data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# --------------------------Views ---------------------------------------
