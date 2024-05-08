from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from account.models import DriverProfile
from account.permissions import IsAuthenticatedCustomer, IsDriver
from trips.models import DriverOffers, Trips, Comment
from trips.serializers.trips_serializers import (
    InputTripSerializer,
    DriverInputTripFinishSerializer,
    CommentSerializer,
)
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import ValidationError
from drf_spectacular.utils import extend_schema


class OrderTrips(APIView):
    permission_classes = [
        IsAuthenticatedCustomer,
    ]

    def post(self, request):
        customer = request.user.customerprofile
        serializer = InputTripSerializer(data=request.data)
        if serializer.is_valid():
            offer = DriverOffers.objects.get(id=request.data.get("id"))

            Trips.objects.create(
                driver=offer.driver,
                driver_offers=offer,
                customer=customer,
                start_time=offer.start_offer_time.hour,
                cost=offer.price,
            )
            # Close another offer
            # Change Driver status
            # Add Discount Code Later

            response = {
                "driver": offer.driver.full_name,
                "car": offer.driver.car,
                "cost": offer.price,
                "end_key": offer.end_key,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class DriverTripsFinish(APIView):
    permission_classes = [
        IsDriver,
    ]

    def patch(self, request):
        serializer = DriverInputTripFinishSerializer(data=request.data)
        if serializer.is_valid():
            is_end = Trips.objects.filter(
                id=request.data.get("id"), is_end=False
            ).update(is_end=True)
            is_updated = DriverProfile.objects.filter(
                user=request.user, status="traveling"
            ).update(status="No-travel")
            if is_updated and is_end:
                response = {"msg": "your Trips Finish"}
                return Response(response, status=status.HTTP_202_ACCEPTED)
            else:
                raise ValidationError("You Dont Have Active travel")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TripsView(APIView):

    def post(self, request):
        pass


class CustomerCommentView(APIView):
    class CreateOutputSerializer(serializers.Serializer):
        msg = serializers.CharField()

    permission_classes = [IsAuthenticatedCustomer]

    @extend_schema(responses=CommentSerializer)
    def get(self, request):
        comments = Comment.objects.filter(
            customer=request.user.customerprofile, is_show=True
        )
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=CommentSerializer, responses=CreateOutputSerializer)
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"msg": "comment save successfully"}, status=status.HTTP_201_CREATED
        )


class CustomerCommentDetailView(APIView):
    class DeleteOutputSerializer(serializers.Serializer):
        msg = serializers.CharField()

    permission_classes = [IsAuthenticatedCustomer]

    @extend_schema(responses=CommentSerializer)
    def get(self, request, id):
        comments = get_object_or_404(
            Comment, id=id, customer=request.user.customerprofile, is_show=True
        )
        serializer = CommentSerializer(comments)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=DeleteOutputSerializer)
    def delete(self, request, id):
        comments = get_object_or_404(
            Comment, id=id, customer=request.user.customerprofile, is_show=True
        )
        comments.is_show = False
        comments.save()
        return Response(
            {"msg": "comment delete successfully"}, status=status.HTTP_200_OK
        )
