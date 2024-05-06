from rest_framework import serializers
from trips.models import Trips

class TripSerializers(serializers.ModelSerializer):
    model = Trips
    fields = []