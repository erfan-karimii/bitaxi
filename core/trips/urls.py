from django.urls import path
from trips.views.driver_offers import DriverOfferViewForDriver,ListDriverOffer,DetailDriverOffer

app_name = "trips"

urlpatterns = [
    path('driver_offers/',DriverOfferViewForDriver.as_view(),name='driver_offer'),
    path('offers/',ListDriverOffer.as_view(),name='offer'),
    path('offer/<int:id>/',DetailDriverOffer.as_view(),name='offer_detail')
]