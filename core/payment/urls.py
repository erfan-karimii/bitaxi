from django.urls import path
from .views import DiscountView , DiscountDetailView

urlpatterns = [
    path('discount/',DiscountView.as_view(),name='discount'),
    path('discount_detail/<str:code>',DiscountDetailView.as_view(),name='discount_detail'),

]
