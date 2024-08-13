from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from account.models import User, CustomerProfile
from utils.loggers import error_logger


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
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
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                error_logger.error(msg)
                raise serializers.ValidationError(msg, code="authorization")
            
            if not user.is_verified:
                msg = _("Please verify your email address first.")
                error_logger.error(msg)
                raise serializers.ValidationError(msg, code="authorization")

            if not user.is_customer:
                msg = _("User is Not Valid Customer.")
                error_logger.error(msg)
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "email" and "password".')
            error_logger.error(msg)
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class RegisterCustomerSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ("email", "password", "password2")

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password2"):
            msg = "first and second password did'nt match"
            error_logger.error(msg)
            raise serializers.ValidationError({"password": msg})
        return super().validate(attrs)


class CustomerResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, max_length=250)
    new_password2 = serializers.CharField(
        required=True, write_only=True, max_length=250
    )

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password2"):
            msg = "Passowrd Does not same"
            error_logger.error(msg)
            raise serializers.ValidationError({"password": "Passowrd Does not same"})

        return super().validate(attrs)


class CustomerProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ["first_name", "last_name", "cash_bank"]


class CustomerProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ["first_name", "last_name"]

    