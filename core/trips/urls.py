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
    DriverComment,
    DriverCommentDetailView,
    CancelTripView
)

app_name = "trips"

urlpatterns = [
    path("offers/driver/list/", DriverOfferViewForDriver.as_view(), name="driver_offer"),
    path("offers/list/", ListDriverOffer.as_view(), name="offer"),
    path("offer/<int:id>/", DetailDriverOffer.as_view(), name="offer_detail"),
    path("offer/order/", OrderTrips.as_view(), name="orderoffer"),
    path("finish/", DriverTripsFinish.as_view(), name="finishtrips"),
    path("comment/", CustomerCommentView.as_view(), name="customer_comment"),
    path(
        "comment/<int:id>/",
        CustomerCommentDetailView.as_view(),
        name="customer_comment_detail",
    ),
    path(
        "comment/superuser/list", SuperuserCommentView.as_view(), name="superuser_comment"
    ),
    path(
        "comment/<int:id>/superuser",
        SuperuserCommentDetailView.as_view(),
        name="superuser_comment_detail",
    ),
    path("comment/driver/", DriverComment.as_view(), name="driver_comment"),
    path(
        "comment/<int:id>/driver",
        DriverCommentDetailView.as_view(),
        name="driver_comment_detail",
    ),
    path("cancel/<int:id>/", CancelTripView.as_view(), name="cancel_trip"),

]
