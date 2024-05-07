from rest_framework import serializers
from trips.models import DriverOffers


class DriverOfferSerializers(serializers.ModelSerializer):
    class Meta:
        model = DriverOffers
        exclude = [
            "id",
            "driver",
            "active",
        ]

    def create(self, obj, validated_data):
        return DriverOffers.objects.create(driver=obj, **validated_data)
