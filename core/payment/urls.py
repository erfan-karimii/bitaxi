from django.urls import path
from .views import DiscountView, DiscountDetailView , DeleteDiscountView

app_name = 'payment'

urlpatterns = [
    path("discount/", DiscountView.as_view(), name="discount"),
    path("delete_discount/", DeleteDiscountView.as_view(), name="delete_discount"),

    path(
        "discount_detail/<str:code>",
        DiscountDetailView.as_view(),
        name="discount_detail",
    ),
]
