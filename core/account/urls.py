from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from account.views.customer_views import CustomCustomerAuthToken
from .views import driver_views

urlpatterns = [
    path('api-token-auth/',CustomCustomerAuthToken.as_view(),name='create-user-token'),
    path('driver_signup/',driver_views.DriverSignUP.as_view(),name='DriverSignUP'),
    path('driver_signin/',driver_views.DriverLogin.as_view(),name='DriverSignIn'),
    path('reset_password/',driver_views.ResetPassword.as_view(),name='reset_password'),
]