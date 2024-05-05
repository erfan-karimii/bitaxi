from django.urls import path
from trips.views.driver_offers import DriverOfferView

app_name = "trips"

urlpatterns = [
    path('driver_offers/',DriverOfferView.as_view(),name='driver_offer'),
]