from rest_framework import serializers
from trips.models import Trips,DriverOffers
from rest_framework.validators import ValidationError

class OrderTripSerializer(serializers.ModelSerializer):
    model = Trips
    fields = ['driver','customer','driver_offers','start_time','cost','discount_code','is_cancel']


class InputTripSerializer(serializers.Serializer):
    id = serializers.IntegerField()


    def validate_id(self,value):
        try:
            DriverOffers.objects.get(id=value)
            return value
        except:
            raise ValidationError("Your DriverOffer Dose Not Exists!")


class DriverInputTripFinishSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    end_key = serializers.CharField(max_length=120)


    def validate_id(self,value):
        try:
            Trips.objects.get(id=value)
            return value
        except:
            raise ValidationError("Your Trips Dose Not Exists!")
        
    def validate(self, attrs):
        offer_end_key=Trips.objects.get(id=attrs['id']).driver_offers.end_key
        # offer=DriverOffers.objects.get(id=attrs['id'])
        
        if offer_end_key != attrs['end_key']:
            raise  ValidationError("Your end_key wrong!")
        
        return attrs
        
    # def validate_end_key(self, value):
    #     try:
    #         DriverOffers.objects.
    #         return value
    #     except:
    #         raise ValidationError("Your Trips Dose Not Exists!")
