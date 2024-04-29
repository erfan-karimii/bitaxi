from django.urls import path

from .views import driver_views
from account.views.customer_views import CustomCustomerAuthToken , RegisterCustomerView

urlpatterns = [
    path('api-token-auth/',CustomCustomerAuthToken.as_view(),name='create-user-token'),
    path('driver_signup/',driver_views.DriverSignUP.as_view(),name='DriverSignUP'),
    path('driver_signin/',driver_views.DriverLogin.as_view(),name='DriverSignIn'),
    path('reset_password/',driver_views.ResetPassword.as_view(),name='reset_password'),
    path('api-token-auth/',CustomCustomerAuthToken.as_view(),name='create-user-token'),
    path('register-user/',RegisterCustomerView.as_view(),name='register-user-view'),
    path('forget-password/',driver_views.ForgetPassword.as_view(),name='forget_password'),
    path('custom/<token>/',driver_views.VerifyForgetPassword.as_view(),name='vrify'),
    path('driverprofile/',driver_views.DriverProfileView.as_view(),name='driverprofile')
]