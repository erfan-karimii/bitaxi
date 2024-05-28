from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema
from django.db.models import Sum
from account.permissions import IsAuthenticatedCustomer
from .permissions import IsSuperUser
from .serializers import (
    DiscountSerializer,
    DiscountDetailSerializer,
    DiscountDeleteSerializer,
    PaidTripSerializer,
)
from trips.models import Trips
from .models import Discount, DiscountUserProfile

from django.conf import settings
import requests
import json

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
        DiscountUserProfile.objects.create(
            customer_profile=request.user.customerprofile, discount=discount
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class Paid(APIView):
    permission_classes = [IsAuthenticatedCustomer]

    def get(self, request):
        user = request.user
        trips = Trips.objects.filter(customer=user.customerprofile, is_paid=False)
        serializer = PaidTripSerializer(trips, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        trips = Trips.objects.filter(
            customer=request.user.customerprofile, is_paid=False
        ).aggregate(Sum("cost"))
        # print(trips.cost__sum)
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": trips["cost__sum"],
            "Description": f"from bitaxi",
            "CallbackURL": "http://127.0.0.1:8000/verify/",
        }
        data = json.dumps(data)
        # set content length by data
        headers = {"content-type": "application/json", "content-length": str(len(data))}

        try:
            response = requests.post(
                settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10
            )

            if response.status_code == 200:
                response = response.json()
                if response["Status"] == 100:
                    return Response(
                        {
                            "status": True,
                            "url": settings.ZP_API_STARTPAY
                            + str(response["Authority"]),
                            "authority": response["Authority"],
                        }
                    )
                else:
                    return Response({"status": False, "code": str(response["Status"])})
            return Response(response)

        except requests.exceptions.Timeout:
            return Response({"status": False, "code": "timeout"})
        except requests.exceptions.ConnectionError:
            return Response({"status": False, "code": "connection error"})


class VerifyPaid(APIView):
    @staticmethod
    def is_paid(trips):
        trips.update(is_paid=True)
        # TODO : باقی کارها اینجا نوشته بشه
        # TODO: SEND message for driver Maybe :)
        # ADD this to PAyment Log

    def get(self, request):
        trips = Trips.objects.filter(
            customer=request.user.customerprofile, is_paid=False
        )
        cost = trips.aggregate(Sum("cost"))
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": cost["cost__sum"],
            "Authority": request.GET["Authority"],
        }

        data = json.dumps(data)
        # set content length by data
        headers = {"content-type": "application/json", "content-length": str(len(data))}
        response = requests.post(settings.ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response["Status"] == 100:
                self.is_paid(trips)
                return Response(
                    {
                        "status": True,
                        "RefID": response["RefID"],
                        "message": "your Trips are paid",
                    }
                )
            else:
                return Response(
                    {
                        "status": False,
                        "code": str(response["Status"]),
                        "message": "Try Again later",
                    }
                )
        return Response(response)
