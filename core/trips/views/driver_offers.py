from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from trips.serializers.driver_offers_serializers import DriverOfferSerializers
from account.permissions import IsDriver
from account.models import DriverProfile
from trips.models import DriverOffers

'''
Masoud -- >
            Must wirte a function Check What Driver(User) Does Not Profile
'''

class DriverOfferView(APIView):
    permission_classes=[IsDriver,]
    def post(self,request):
        user_profile=DriverProfile.objects.get(user=request.user)
        if user_profile.status == "No-travel":
            serializer = DriverOfferSerializers(data=request.data)
            if serializer.is_valid():
                serializer.create(obj=user_profile,validated_data=serializer.validated_data)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg":"Your current Travel Not Finish"},status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request):
        user_profile=DriverProfile.objects.get(user=request.user)
        objects =DriverOffers.objects.filter(driver = user_profile,active=True )
        serializer = DriverOfferSerializers(objects,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)