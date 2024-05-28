from django.urls import reverse
from django.contrib.auth.hashers import make_password

from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from model_bakery import baker

from account.models import User


class TestCustomerLoginView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("account:create-user-token")
        self.client = APIClient()

        self.customer_password = "1"
        self.customer_email = "test@test.com"
        self.customer = baker.make(
            User,
            email=self.customer_email,
            password=make_password(self.customer_password),
            is_customer=True,
            is_verified=True,
        )

        self.not_customer_password = "2"
        self.not_customer_email = "test2@test.com"
        self.not_customer = baker.make(
            User,
            email=self.not_customer_email,
            password=make_password(self.not_customer_password),
            is_customer=False,
        )

    def test_successful_login(self):
        data = {"email": self.customer_email, "password": self.customer_password}
        response = self.client.post(self.url, data=data, format="json")

        self.assertEqual(response.data.get("email"), self.customer_email)
        self.assertEqual(
            response.data.get("token"), Token.objects.get(user=self.customer).key
        )
        self.assertTrue(Token.objects.filter(user=self.customer).exists())


class TestRegisterCustomerView(APITestCase):
    def setUp(self):
        self.valid_data = {
            "email": "admin@admin.com",
            "password": "12",
            "password2": "12",
        }
        self.un_valid = {
            "email": "admin@admin.com",
            "password": "122",
            "password2": "12",
        }
        self.url = reverse("account:register_user_view")

    def test_valid_customer_signup(self):
        email = self.valid_data.get("email")
        response = self.client.post(self.url, data=self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["msg"], f"Your account has been created successfully. Please check your email to confirm your email address"
        )

    def test_unvalid_driver_signup(self):

        response = self.client.post(self.url, data=self.un_valid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestCustomerResetPasswordView(APITestCase):
    def setUp(self) -> None:
        self.customer = User.objects.create_user(
            email="test@test.com", password="1", is_customer=True,is_verified=True
        )
        self.token = Token.objects.create(user=self.customer)
        self.password1 = "1"
        self.password2 = "2"
        self.url = reverse("account:customer_reset_password")
        self.client = APIClient()

    def test_match_password(self):
        data = {"new_password": self.password1, "new_password2": self.password1}
        headers = {"Authorization": f"Token {self.token.key}"}
        response = self.client.patch(self.url, data, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data.get("msg"), "User password updated successfully")

    def test_unmatch_password(self):
        data = {"new_password": self.password1, "new_password2": self.password2}
        headers = {"Authorization": f"Token {self.token.key}"}
        response = self.client.patch(self.url, data, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assert
        # self.assertEqual(response.data.get("msg"),"User password updated successfully")


class TestCustomerForgetPasswordView(APITestCase):
    def setUp(self) -> None:
        self.user_email1 = "test@test.com"
        self.user_email2 = "test2@test.com"
        self.not_user_email = "test3@test.com"

        self.customer_with_token = User.objects.create_user(
            email=self.user_email1, password="1", is_customer=True
        )
        self.customer_without_token = User.objects.create_user(
            email=self.user_email2, password="2", is_customer=True
        )
        self.token = Token.objects.create(user=self.customer_with_token)

        self.url = reverse("account:customer_forget_password")
        self.client = APIClient()

    def test_unvalid_email(self):
        response = self.client.post(self.url, data={"email": "test"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.data, {"email": ["Enter a valid email address."]})

    def test_unvalid_user(self):
        response = self.client.post(self.url, data={"email": self.not_user_email})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.data, {"msg": "Email Does Not exist"})

    def test_valid_user_exist_token(self):
        response = self.client.post(self.url, data={"email": self.user_email1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.count(), 1)
        self.assertDictEqual(response.data, {"msg": "recovery email send successfully"})

    def test_valid_user_not_exist_token(self):
        response = self.client.post(self.url, data={"email": self.user_email2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.count(), 2)
        self.assertDictEqual(response.data, {"msg": "recovery email send successfully"})

 
class TestCustomerVerifyForgetPasswordView(APITestCase):
    def setUp(self) -> None:
        self.customer = User.objects.create_user(
            email="test@test.com", password="1", is_customer=True,is_verified=True
        )
        self.token = Token.objects.create(user=self.customer).key
        self.valid_url = reverse(
            "account:customer_verify_password", kwargs={"token": self.token}
        )
        self.unvalid_url = reverse(
            "account:customer_verify_password", kwargs={"token": "wrong token"}
        )
        self.client = APIClient()

    def test_valid_token(self):
        response = self.client.post(self.valid_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.data, {"msg": "success fully return", "token": self.token}
        )

    def test_unvalid_token(self):
        response = self.client.post(self.unvalid_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.data, {"msg": "time error"})


class TestResendEmailConfirmView(APITestCase):
    def setUp(self) -> None:
        self.verified_customer = User.objects.create_user(
            email="test@test.com", password="1", is_customer=True,is_verified=True
        )
        self.verified_customer_token = Token.objects.create(user=self.verified_customer).key
        
        self.unverified_customer = User.objects.create_user(
            email="test1@test.com", password="11", is_customer=True,is_verified=False
        )
        self.unverified_customer_token = Token.objects.create(user=self.unverified_customer).key
        
        self.url = reverse("account:resend_conf_email")
        self.client = APIClient()
    
    def test_post_verified_user(self):
        response = self.client.post(self.url,{"email":"test@test.com"})
        
        self.assertEqual(response.status_code,400)
    
    def test_post_unverified_user(self):
        response = self.client.post(self.url,{"email":"test1@test.com"})
                
        self.assertEqual(response.status_code,200)
    

class TestConfirmEmailAddressView(APITestCase):
    def setUp(self) -> None:
        self.unverified_customer = User.objects.create_user(
            email="test2@test.com", password="11", is_customer=True,is_verified=False,Token=1
        )
        self.unverified_customer_token = Token.objects.create(user=self.unverified_customer).key
        
        self.client = APIClient()
    
    def test_post_unverified_user(self):
        url = reverse("account:confirm_email",kwargs={'email':'test2@test.com','token':1})
        response = self.client.post(url)
                
        
        self.unverified_customer.refresh_from_db()
        self.assertEqual(response.status_code,200)
        self.assertTrue(self.unverified_customer.is_verified)