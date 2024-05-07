from rest_framework.views import APIView
from account.permissions import IsAuthenticatedCustomer
from trips.models import DriverOffers,Trips
from trips.serializers.trips_serializers import InputTripSerializer,DriverInputTripFinishSerializer
from rest_framework.response import Response
from rest_framework import status

class OrderTrips(APIView):
    permission_classes = [IsAuthenticatedCustomer,]
    def post(self,request):
        customer = request.user.customerprofile
        serializer = InputTripSerializer(data=request.data)
        if serializer.is_valid():
            offer = DriverOffers.objects.get(id=request.data.get('id'))
            
            Trips.objects.create(driver=offer.driver,driver_offers=offer,customer=customer,start_time=offer.start_offer_time.hour,cost=offer.price)
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
    permission_classes = [IsAuthenticatedCustomer,]
    def patch(self,request):
        serializer = DriverInputTripFinishSerializer(data=request.data)
        if serializer.is_valid():
            Trips.objects.filter(id=request.data.get('id')).update(is_end=True)
            response = {
                'msg':'your Trips Finish'
            }
            return Response(response,status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)






class TripsView(APIView):
    
    def post(self,request):
        pass