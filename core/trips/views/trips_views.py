from rest_framework.views import APIView
from account.models import DriverProfile
from account.permissions import IsAuthenticatedCustomer,IsDriver
from trips.models import DriverOffers,Trips
from trips.serializers.trips_serializers import InputTripSerializer,DriverInputTripFinishSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import ValidationError

class OrderTrips(APIView):
    permission_classes = [IsAuthenticatedCustomer,]



    def post(self,request):
        customer = request.user.customerprofile
        serializer = InputTripSerializer(data=request.data)
        if serializer.is_valid():
            offer = DriverOffers.objects.get(id=request.data.get('id'))
            
            Trips.objects.create(driver=offer.driver,driver_offers=offer,customer=customer,start_time=offer.start_offer_time.hour,cost=offer.price)
            # Close another offer
            # Change Driver status
            # Add Discount Code Later
            
            response = {
                'driver':offer.driver.full_name,
                'car':offer.driver.car,
                'cost':offer.price,
                'end_key':offer.end_key
            }
            return Response(response,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)



class DriverTripsFinish(APIView):
    permission_classes = [IsDriver,]
    def patch(self,request):
        serializer = DriverInputTripFinishSerializer(data=request.data)
        if serializer.is_valid():
            is_end=Trips.objects.filter(id=request.data.get('id'),is_end=False).update(is_end=True)
            is_updated= DriverProfile.objects.filter(user=request.user,status='traveling').update(status="No-travel")
            if is_updated and is_end:
                response = {
                    'msg':'your Trips Finish'
                }
                return Response(response,status=status.HTTP_202_ACCEPTED)
            else:
                raise ValidationError("You Dont Have Active travel")
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)






class TripsView(APIView):
    
    def post(self,request):
        pass