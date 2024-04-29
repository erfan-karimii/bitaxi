from django.urls import path

from .views import driver_views
from account.views.customer_views import CustomerLogin , RegisterCustomerView , CustomerResetPassword , CustomerForgetPassword, CustomerProfileView

urlpatterns = [
    path('driver_signup/',driver_views.DriverSignUP.as_view(),name='DriverSignUP'),
    path('druseriver_signin/',driver_views.DriverLogin.as_view(),name='DriverSignIn'),
    path('reset_password/',driver_views.ResetPassword.as_view(),name='reset_password'),
    path('forget-password/',driver_views.ForgetPassword.as_view(),name='forget_password'),
    path('custom/<token>/',driver_views.VerifyForgetPassword.as_view(),name='vrify'),
    path('driverprofile/',driver_views.DriverProfileView.as_view(),name='driverprofile'),
    
]


customer_urlpatterns = [
    path('customer-login/',CustomerLogin.as_view(),name='create-user-token'),
    path('customer-register/',RegisterCustomerView.as_view(),name='register_user_view'),
    path('customer-reset-password/',CustomerResetPassword.as_view(),name='customer_reset_password'),
    path('customer-forget-password/',CustomerForgetPassword.as_view(),name='customer_forget_password'),
    path('customer-profile/',CustomerProfileView.as_view(),name='customer_profile'),
]


urlpatterns += customer_urlpatterns