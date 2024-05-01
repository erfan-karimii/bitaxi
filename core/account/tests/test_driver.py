from django.test import TestCase
from account.models import User
from django.test.client import RequestFactory
from account.permissions import IsDriver
from account.views.driver_views import DriverProfileView
from django.urls import reverse
from account.serializers.driver_serializers import InputRegisterSerializers
from rest_framework.validators import ValidationError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, force_authenticate

# Permission

class IsDriverPermissionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(email='idnex@gmail.com',password='12', is_driver=True)
        self.user2 = User.objects.create_user(email='test@gmail.com',password='12', is_customer=True)
        self.view = DriverProfileView.as_view()
        self.permission = IsDriver()

    def test_driver_permission(self):
        urls=self.factory.get(reverse('account:driverprofile'))
        urls.user = self.user1

        self.assertTrue(self.permission.has_permission(urls, self.view))

    def test_no_driver(self):
        urls = self.factory.get(reverse('account:driverprofile'))
        urls.user = self.user2
        self.assertFalse(self.permission.has_permission(urls,self.view))


# ------------------------- Serializers ------------------------------

class InputRegisterSerializersTest(TestCase):
    def setUp(self):
        self.valid_data = {'email':"admin@admin.com","password":"12","password1":"12"}
        self.invalid_data = {'email':"","password":"12","password1":"12"}


    def test_valid_data(self):
        serializer = InputRegisterSerializers(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        serializer = InputRegisterSerializers(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_password_not_same(self):
        data = {'email':"admin@admin.com","password":"12","password1":"12"}
        serializers = InputRegisterSerializers()

        with self.assertRaises(ValidationError) as context:
            serializers.validate(data)
        self.assertIn("Passowrd Does not same",str(context.exception.detail))

    
    def test_password_same(self):
        data = {'email':"admin@admin.com","password":"12","password1":"12"}
        serializer = InputRegisterSerializers()
        self.assertEqual(serializer.validate(attrs=data),data)

# ------------------------- Serializers ------------------------------


# --------------------------Views --------------------------------------

class TestDriverSignUp(TestCase):
    def setUp(self):
        self.valid_data = {'email':"admin@admin.com","password":"12","password1":"12"}
        self.un_valid = {'email':"admin@admin.com","password":"122","password1":"12"}
        self.url = reverse('account:DriverSignUP')
    
    def test_valid_driver_signup(self):

        response = self.client.post(self.url,data=self.valid_data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
        self.assertEqual(response.data['email'],"admin@admin.com")
        self.assertEqual(response.data,{"email":"admin@admin.com","message":"اکانت شما با موفقیت ساخته شد"})    

    def test_unvalid_driver_signup(self):

        response = self.client.post(self.url,data=self.un_valid)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)





class TestDriverSignIn(TestCase):
    def setUp(self):
        User.objects.create_user(email='index@gmail.com', password='password123',is_driver=True)
        User.objects.create_user(email='customer@gmail.com', password='password123',is_driver=False)
        self.url = reverse("account:DriverSignIn")
    
    def test_valid_login(self):
        data = {"email":'index@gmail.com', "password":'password123'}
        response=self.client.post(self.url,data=data)
        # self.assertEqual(response)
        self.assertEqual(response.data['email'],"index@gmail.com")

    def test_unvalid_login_user_does_not_exists(self):
        unvalid_data = {"email":'tset@gmail.com', "password":'password123'}
        response=self.client.post(self.url,data=unvalid_data)
        self.assertIn('Unable to log in with provided credentials.',str(response._container))

    def test_unvalid_login_user_not_driver(self):
        unvalid_data = {"email":'customer@gmail.com', "password":'password123'}
        response = self.client.post(self.url,data=unvalid_data)
        self.assertIn('You are Not Driver!',str(response.content))




class ResetPasswordTest(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(email='index@gmail.com', password='password123@',is_driver=True)
        self.token = Token.objects.create(user=self.user)
        self.url = reverse("account:reset_password")
    
    def test_valid_reset_password(self):
        data = {"new_password": 'password1234', 'new_password1': 'password1234'}
        
        headers = {'Authorization': f'Token {self.token.key}'}
        response = self.client.put(self.url, data=data,headers=headers)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        
        self.assertIn("Your Password Changed",response.content.decode('utf-8'))


    def test_unvalid_reset_password(self):
        data = {"new_password": 'password34', 'new_password1': 'password1234'}
        headers = {'Authorization': f'Token {self.token.key}'}

        response = self.client.put(path=self.url,data=data,headers=headers)
        self.assertIn("Passowrd Does not same",response.content.decode('utf-8'))
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


    
# --------------------------Views ---------------------------------------