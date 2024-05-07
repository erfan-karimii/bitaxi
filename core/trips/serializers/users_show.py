from rest_framework import serializers
from account.models import DriverProfile




class DriverShowForUserSerializer(serializers.ModelSerializer):
    """
    this serializers Show Driver information for another users
    info contains --> fname lname car ...
    but we dont show his cash_bank or his id
    """
    class Meta:
        model = DriverProfile
        fields = ['first_name','last_name','image','car','count_trip']

