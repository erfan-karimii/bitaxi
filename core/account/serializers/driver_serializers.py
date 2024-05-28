from django.db.models.fields import BinaryField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

from rest_framework.validators import ValidationError
from rest_framework import serializers

from account.models import User , DriverProfile

class InputRegisterSerializers(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=250, write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password1",
        ]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise ValidationError("Passowrd Does not same")

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data, is_driver=True)


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
    )
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")

            if not user.is_driver:
                msg = _("You are Not Driver!")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, max_length=250)
    new_password1 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise ValidationError("Passowrd Does not same")

        return super().validate(attrs)

    def update(self, validated_data):
        user = self.context["request"].user
        user.set_password(validated_data["new_password"])
        user.save()
        return user


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)


class DriverProfileSerializers(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = DriverProfile
        exclude = ["status", "id", "created_at", "updated_at", "user","count_trip"]
        # fields = "__all__"

    def get_email(self, obj):
        return obj.user.email


    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.cash_bank = validated_data.get("cash_bank", instance.cash_bank)
        instance.image = validated_data.get("image", instance.image)
        
        if validated_data.get("ID_image") is not None:
            instance.ID_image = DriverProfile.compress_image(validated_data.get("ID_image"))        
            
         
        instance.car = validated_data.get("car", instance.car)

        instance.save()

        return instance
