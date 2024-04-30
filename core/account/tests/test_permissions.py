from rest_framework.test import APITestCase , DjangoRequestFactory
from unittest import mock

from account.permissions import IsAuthenticatedCustomer
from account.models import User
from model_bakery import baker

class TestIsAuthenticatedCustomerPermission(APITestCase):
    def setUp(self) -> None:
        self.mock_request = mock.Mock(spec=DjangoRequestFactory)
    
    def test_customer_access(self):
        customer_user = baker.make(User,is_customer=True)
        self.mock_request.user = customer_user
        permission_instance = IsAuthenticatedCustomer()
        
        self.assertTrue(permission_instance.has_permission(request=self.mock_request,view=None))
        
    
    def test_not_customer_access(self):
        not_customer_user = baker.make(User,is_customer=False)
        self.mock_request.user = not_customer_user
        permission_instance = IsAuthenticatedCustomer()
        
        self.assertFalse(permission_instance.has_permission(request=self.mock_request,view=None))


