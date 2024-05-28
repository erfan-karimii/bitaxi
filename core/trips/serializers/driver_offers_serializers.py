import random

from rest_framework import serializers
from trips.models import DriverOffers


class DriverOfferSerializers(serializers.ModelSerializer):
    class Meta:
        model = DriverOffers
        exclude = [
            "id",
            "driver",
            "active",
            "end_key"
        ]

    def create(self, obj, validated_data):
        end_key = random.randint(1000,100000)
        return DriverOffers.objects.create(driver=obj,end_key=end_key, **validated_data)
