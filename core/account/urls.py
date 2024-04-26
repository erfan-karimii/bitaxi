from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from account.views.customer_views import CustomCustomerAuthToken , RegisterCustomerView

urlpatterns = [
    path('api-token-auth/',CustomCustomerAuthToken.as_view(),name='create-user-token'),
    path('register-user/',RegisterCustomerView.as_view(),name='register-user-view'),
    
]
