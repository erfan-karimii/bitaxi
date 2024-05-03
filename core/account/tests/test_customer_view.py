from django.urls import reverse
from django.contrib.auth.hashers import make_password

from rest_framework.test import APIClient , APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from model_bakery import baker

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
    
    
        
class TestCustomerResetPasswordView(APITestCase):
    def setUp(self) -> None:
        self.customer = User.objects.create_user(email='test@test.com', password='1',is_customer=True)
        self.token = Token.objects.create(user=self.customer)
        self.password1 = "1"
        self.password2 = "2"
        self.url = reverse("account:customer_reset_password")
        self.client = APIClient()

    
    def test_match_password(self):
        data = {
            "new_password" : self.password1,
            "new_password2" : self.password1
        }
        headers = {'Authorization': f'Token {self.token.key}'}
        response = self.client.patch(self.url,data,headers=headers)
        
        self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data.get("msg"),"User password updated successfully")
    
    def test_unmatch_password(self):
        data = {
            "new_password" : self.password1,
            "new_password2" : self.password2
        }
        headers = {'Authorization': f'Token {self.token.key}'}
        response = self.client.patch(self.url,data,headers=headers)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        # self.assert
        # self.assertEqual(response.data.get("msg"),"User password updated successfully")
        
        
        