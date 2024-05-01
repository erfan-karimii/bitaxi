from django.urls import reverse
from django.contrib.auth.hashers import make_password

from rest_framework.test import APIClient , APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from model_bakery import baker

from account.views.customer_views import CustomerLoginView, RegisterCustomerView, CustomerResetPasswordView, CustomerForgetPasswordView, CustomerVerifyForgetPasswordView, CustomerProfileView
from account.models import User

class TestCustomerLoginView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('account:create-user-token')
        self.client = APIClient()
        
        self.customer_password = "1"
        self.customer_email = 'test@test.com'
        self.customer = baker.make(User,email=self.customer_email,
                                   password=make_password(self.customer_password),is_customer=True,is_verified=True)
        
        self.not_customer_password = "2"
        self.not_customer_email = 'test2@test.com'      
        self.not_customer = baker.make(User,email=self.not_customer_email,
                                   password=make_password(self.not_customer_password),is_customer=False)
        
        
    def test_successful_login(self):
        data = {'email':self.customer_email,'password':self.customer_password}
        response = self.client.post(self.url,data=data,format='json')
        
        self.assertEqual(response.data.get('email'),self.customer_email)
        self.assertEqual(response.data.get('token'),Token.objects.get(user=self.customer).key)
        self.assertTrue(Token.objects.filter(user=self.customer).exists())
        
    

        
    

class TestRegisterCustomerView(APITestCase):
    def setUp(self):
        self.valid_data = {'email':"admin@admin.com","password":"12","password2":"12"}
        self.un_valid = {'email':"admin@admin.com","password":"122","password2":"12"}
        self.url = reverse('account:register_user_view')
    
    def test_valid_driver_signup(self):
        email = self.valid_data.get('email')
        response = self.client.post(self.url,data=self.valid_data)

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['created'],f'user with {email} email address created')

    def test_unvalid_driver_signup(self):

        response = self.client.post(self.url,data=self.un_valid)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    
        
        
    
    
