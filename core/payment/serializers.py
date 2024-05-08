from rest_framework import serializers
from .models import Discount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"


class DiscountDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    # class Meta:
    #     model = Discount
    #     fields = ("id",)


class DiscountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ("code", "discount")
