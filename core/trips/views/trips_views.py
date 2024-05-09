from django.db.models import F
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.views import APIView
from account.models import CustomerProfile, DriverProfile
from account.permissions import IsAuthenticatedCustomer, IsDriver
from trips.models import DriverOffers, Trips
from trips.serializers.trips_serializers import (
    InputTripSerializer,
    DriverInputTripFinishSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import ValidationError
from drf_spectacular.utils import extend_schema

from account.models import DriverProfile, User
from account.permissions import IsAuthenticatedCustomer, IsDriver, IsSuperuser
from trips.models import DriverOffers, Trips, Comment
from trips.serializers.trips_serializers import (
    InputTripSerializer,
    DriverInputTripFinishSerializer,
    UserCommentSerializer,
    SuperuserCommentSerializer,
)
from utils.loggers import general_logger


class OrderTrips(APIView):
    permission_classes = [
        IsAuthenticatedCustomer,
    ]

    @staticmethod
    def create_trips(offer: DriverOffers, customer: CustomerProfile) -> None:
        Trips.objects.create(
            driver=offer.driver,
            driver_offers=offer,
            customer=customer,
            start_time=offer.start_offer_time.hour,
            cost=offer.price,
        )

    @staticmethod
    def close_all_driver_offer(driver: DriverProfile) -> None:
        DriverOffers.objects.filter(driver=driver).update(active=False)

    @staticmethod
    def change_driver_status(driver: DriverProfile) -> None:
        DriverProfile.objects.filter(user=driver.user).update(status="traveling")

    def post(self, request):
        customer = request.user.customerprofile
        serializer = InputTripSerializer(data=request.data)
        if serializer.is_valid():
            offer = DriverOffers.objects.get(id=request.data.get("id"))
            self.create_trips(offer, customer)
            self.close_all_driver_offer(driver=offer.driver)
            self.change_driver_status(driver=offer.driver)
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

    @staticmethod
    def finish_trips(id)-> bool:
        is_end = Trips.objects.filter(id=id, is_end=False).update(is_end=True)
        return is_end

    @staticmethod
    def change_driver_status(user)-> bool:
        is_updated = DriverProfile.objects.filter(user=user, status="traveling").update(
            status="No-travel"
        )
        return is_updated
    
    @staticmethod
    def add_trip_count(driver):
        # obj=DriverProfile.objects.get(user=driver)
        # obj.count_trip += 1
        # obj.save()
        obj=DriverProfile.objects.get(user=driver)
        obj.count_trip = F('count_trip') + 1
        obj.save()
        

    def patch(self, request):
        serializer = DriverInputTripFinishSerializer(data=request.data)
        if serializer.is_valid():
            is_end = self.finish_trips(id=request.data.get("id"))
            is_updated = self.change_driver_status(user=request.user)

            if is_updated and is_end:
                response = {"msg": "your Trips Finish"}
                self.add_trip_count(driver = request.user)
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

    @extend_schema(responses=UserCommentSerializer)
    def get(self, request):
        comments = Comment.objects.filter(
            customer=request.user.customerprofile, is_show=True
        )
        serializer = UserCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=UserCommentSerializer, responses=CreateOutputSerializer)
    def post(self, request):
        serializer = UserCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"msg": "comment save successfully"}, status=status.HTTP_201_CREATED
        )


class CustomerCommentDetailView(APIView):
    class DeleteOutputSerializer(serializers.Serializer):
        msg = serializers.CharField()

    permission_classes = [IsAuthenticatedCustomer]

    @extend_schema(responses=UserCommentSerializer)
    def get(self, request, id):
        comment = get_object_or_404(
            Comment, id=id, customer=request.user.customerprofile, is_show=True
        )
        serializer = UserCommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=DeleteOutputSerializer)
    def delete(self, request, id):
        comment = get_object_or_404(
            Comment, id=id, customer=request.user.customerprofile, is_show=True
        )
        comment.is_show = False
        comment.save()
        return Response(
            {"msg": "comment delete successfully"}, status=status.HTTP_200_OK
        )


class SuperuserCommentView(APIView):
    permission_classes = [IsSuperuser]

    @extend_schema(responses=SuperuserCommentSerializer)
    def get(self, request):
        comments = Comment.objects.all()
        serializer = SuperuserCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SuperuserCommentDetailView(APIView):
    class PatchInputSerializer(serializers.Serializer):
        show = serializers.BooleanField()

    class PatchOutputSerializer(serializers.Serializer):
        msg = serializers.CharField()

    permission_classes = [IsSuperuser]

    @extend_schema(request=PatchInputSerializer, responses=PatchOutputSerializer)
    def patch(self, request, id):
        comment = get_object_or_404(Comment, id=id)
        serializer = self.PatchInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment.is_show = serializer.validated_data.get("show")
        comment.save()
        return Response(
            {"msg": "comment change successfully"}, status=status.HTTP_202_ACCEPTED
        )

    def delete(self, request, id):
        comment = get_object_or_404(Comment, id=id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DriverComment(APIView):
    permission_classes = [IsDriver]

    @extend_schema(responses=UserCommentSerializer)
    def get(self, request):
        comments = Comment.objects.filter(
            driver=request.user.driverprofile, is_show=True
        )
        serializer = UserCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DriverCommentDetailView(APIView):
    class InputReportSerializer(serializers.Serializer):
        msg = serializers.CharField(max_length=254)

    class OutputReportSerializer(serializers.Serializer):
        msg = serializers.CharField(max_length=254)

    permission_classes = [IsDriver]

    @staticmethod
    def send_report_email(msg, email, comment_id):
        superusers_emails = User.objects.filter(is_superuser=True).values_list(
            "email", flat=True
        )
        send_mail(
            subject="forget password",
            message=f"email :{email}\ncomment id :{comment_id}\nmsg :{msg}",
            from_email="admin@admin.com",
            recipient_list=superusers_emails,
            fail_silently=True,
        )
        general_logger.info(f"recovery email to {superusers_emails} send successfully")

    @extend_schema(request=InputReportSerializer, responses=OutputReportSerializer)
    def post(self, request, id):
        comment = get_object_or_404(
            Comment, id=id, driver=request.user.driverprofile, is_show=True
        )
        serializer = self.InputReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.send_report_email(
            serializer.validated_data.get("msg"), request.user.email, comment.id
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
