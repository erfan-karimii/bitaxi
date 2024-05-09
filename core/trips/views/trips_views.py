from django.db.models import F
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
