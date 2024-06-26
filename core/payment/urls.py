from django.urls import path
from .views import (
    DiscountView,
    DiscountDetailView,
    DeleteDiscountView,
    Paid,
    VerifyPaid,
)

app_name = "payment"

urlpatterns = [
    path("discount/", DiscountView.as_view(), name="discount"),
    path("discount/delete/", DeleteDiscountView.as_view(), name="delete_discount"),
    path(
        "discount/<str:code>",
        DiscountDetailView.as_view(),
        name="discount_detail",
    ),
    path("pay-trips/", Paid.as_view(), name="paid"),
    path("verify/", VerifyPaid.as_view(), name="verifypaid"),
]
