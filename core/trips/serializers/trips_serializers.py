from rest_framework import serializers
from trips.models import Trips, DriverOffers, Comment
from rest_framework.validators import ValidationError


class OrderTripSerializer(serializers.ModelSerializer):
    model = Trips
    fields = [
        "driver",
        "customer",
        "driver_offers",
        "start_time",
        "cost",
        "discount_code",
        "is_cancel",
    ]


class InputTripSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate_id(self, value):
        try:
            DriverOffers.objects.get(id=value)
            return value
        except:
            raise ValidationError("Your DriverOffer Dose Not Exists!")


class DriverInputTripFinishSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    end_key = serializers.CharField(max_length=120)

    def validate_id(self, value):
        try:
            Trips.objects.get(id=value)
            return value
        except:
            raise ValidationError("Your Trip do Not Exists!")
        
            raise ValidationError("Your Trips Dose Not Exists!")

    def validate(self, attrs):
        offer_end_key = Trips.objects.get(id=attrs["id"]).driver_offers.end_key

        if offer_end_key != attrs["end_key"]:
            raise ValidationError("Your end_key wrong!")

        return attrs

class UserCommentSerializer(serializers.ModelSerializer):
    trip_start_time = serializers.ReadOnlyField(source="trip.start_time")
    trip_is_end = serializers.ReadOnlyField(source="trip.is_end")
    trip_is_cancel = serializers.ReadOnlyField(source="trip.is_cancel")
    driver_offers_id = serializers.ReadOnlyField(source="trip.driver_offers_id")

    class Meta:
        model = Comment
        fields = (
            "customer",
            "driver",
            "trip",
            "trip_start_time",
            "trip_is_end",
            "trip_is_cancel",
            "driver_offers_id",
            "text",
            "score",
            "created_at",
        )
        read_only_fields = ("created_at",)
        extra_kwargs = {
            "driver": {"write_only": True},
            "trip": {"write_only": True},
            "customer": {"write_only": True},
        }


class SuperuserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

        