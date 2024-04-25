from .views import driver_views
from django.urls import path

urlpatterns = [
    path('signup/',driver_views.DriverSignUP.as_view(),name='DriverSignUP')
    # path('driver_signup/',driver_views.CustomeObtainAuthToken.as_view(),name='driver_signup'),
]
