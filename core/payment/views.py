from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema

from account.permissions import IsAuthenticatedCustomer
from .permissions import IsSuperUser
from .serializers import (
    DiscountSerializer,
    DiscountDetailSerializer,
    DiscountDeleteSerializer,
)
from .models import Discount , DiscountUserProfile

# Create your views here.


class DiscountView(APIView):
    permission_classes = [IsSuperUser]
    serializer_class = DiscountSerializer

    def get(self, request):
        discounts = Discount.objects.all()
        serializer = self.serializer_class(discounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteDiscountView(APIView):
    permission_classes = [IsSuperUser]

    @extend_schema(request=DiscountDeleteSerializer)
    def delete(self, request):
        serializer = DiscountDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        discount_id = serializer.validated_data.get("id")
        is_deleted = Discount.objects.filter(id=discount_id).delete()
        if is_deleted[0]:
            return Response(
                {"discount": "discount deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"detail": "invalid id sent."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DiscountDetailView(APIView):
    serializer_class = DiscountDetailSerializer
    permission_classes = [IsAuthenticatedCustomer]

    def get(self, request, code):
        discount = get_object_or_404(Discount, code=code)
        if not discount.is_still_valid():
            raise serializers.ValidationError({"detail": "discount code expired"})
        serializer = self.serializer_class(discount)
        DiscountUserProfile.objects.create(customer_profile=request.user.customerprofile,discount=discount)
        return Response(serializer.data, status=status.HTTP_200_OK)
