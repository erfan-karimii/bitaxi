from django.urls import path
from trips.views.driver_offers import (
    DriverOfferViewForDriver,
    ListDriverOffer,
    DetailDriverOffer,
)
from trips.views.trips_views import (
    OrderTrips,
    DriverTripsFinish,
    CustomerCommentView,
    CustomerCommentDetailView,
    SuperuserCommentView,
    SuperuserCommentDetailView,
)

app_name = "trips"

urlpatterns = [
    path("driver_offers/", DriverOfferViewForDriver.as_view(), name="driver_offer"),
    path("offers/", ListDriverOffer.as_view(), name="offer"),
    path("offer/<int:id>/", DetailDriverOffer.as_view(), name="offer_detail"),
    path("orderoffer/", OrderTrips.as_view(), name="orderoffer"),
    path("finishtrips/", DriverTripsFinish.as_view(), name="finishtrips"),
    path("customer_comment/", CustomerCommentView.as_view(), name="customer_comment"),
    path(
        "customer_comment_detail/<int:id>/",
        CustomerCommentDetailView.as_view(),
        name="customer_comment",
    ),
    path(
        "superuser_comment/", SuperuserCommentView.as_view(), name="superuser_comment"
    ),
    path(
        "superuser_comment_detail/<int:id>/",
        SuperuserCommentDetailView.as_view(),
        name="superuser_comment_detail",
    ),
]
