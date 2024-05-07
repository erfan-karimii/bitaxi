from rest_framework import serializers 
from .models import Discount

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'

class DiscountDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ("id",)

class DiscountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ("code","discount")
