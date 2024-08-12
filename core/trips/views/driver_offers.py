from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from trips.serializers.driver_offers_serializers import DriverOfferSerializers
from account.permissions import IsDriver, IsAuthenticatedCustomer
from account.models import DriverProfile
from trips.serializers.users_show import DriverShowForUserSerializer
from trips.models import DriverOffers
from drf_spectacular.utils import extend_schema

"""
Masoud -- >
            Must wirte a function Check What Driver(User) Does Not Profile
"""


class DriverOfferViewForDriver(APIView):
    permission_classes = [
        IsDriver,
    ]
    @extend_schema(request=DriverOfferSerializers,responses=DriverOfferSerializers)
    def post(self, request):
        #FIXME: check driver does not have many origin in same time
        user_profile = DriverProfile.objects.get(user=request.user)
        # print(user_profile.status)
        if (user_profile.status == "No-travel") or (user_profile.status == ""):
            serializer = DriverOfferSerializers(data=request.data)
            if serializer.is_valid():
                serializer.create(
                    obj=user_profile, validated_data=serializer.validated_data
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"msg": "Your current Travel Not Finish"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request):
        user_profile = DriverProfile.objects.get(user=request.user)
        objects = DriverOffers.objects.filter(driver=user_profile, active=True)
        serializer = DriverOfferSerializers(objects, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ListDriverOffer(APIView):
    permission_classes = [
        IsAuthenticatedCustomer,
    ]

    class OutPutListSerializer(serializers.ModelSerializer):
        show = serializers.SerializerMethodField(read_only=True)

        class Meta:
            model = DriverOffers
            fields = ["origin", "destination", "price", "show"]

        def get_show(self, obj):
            url = reverse("trips:offer_detail", kwargs={"id": obj.id})
            return self.context.get("request").get_host() + url

    @extend_schema(responses=OutPutListSerializer)
    def get(self, request):
        offers = DriverOffers.objects.filter(active=True)
        serializer = self.OutPutListSerializer(
            offers, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetailDriverOffer(APIView):
    permission_classes = [
        IsAuthenticatedCustomer,
    ]

    class OutPutListSerializer(serializers.ModelSerializer):
        driver = DriverShowForUserSerializer()

        class Meta:
            model = DriverOffers
            exclude = ["id", "active"]

    @extend_schema(responses=DriverShowForUserSerializer)
    def get(self, request, id):
        offer = DriverOffers.objects.get(id=id, active=True)
        serializer = self.OutPutListSerializer(offer)
        return Response(serializer.data, status=status.HTTP_200_OK)
