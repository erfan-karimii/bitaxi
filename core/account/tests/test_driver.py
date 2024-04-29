from django.test import TestCase
from account.models import User
from django.test.client import RequestFactory
from account.permissions import IsCustomer,IsDriver
from account.views.driver_views import DriverProfileView
from django.urls import reverse



class IsDriverPermissionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email='idnex@gmail.com',password='12', is_driver=True)
        self.view = DriverProfileView.as_view()

    def test_driver_permission(self):
        urls=self.factory.get(reverse('driverprofile'))
        urls.user = self.user
        permission = IsDriver()
        self.assertTrue(permission.has_permission(urls, self.view))
        # self.assertTrue(permission.message,)
