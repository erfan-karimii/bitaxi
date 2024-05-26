import random 
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema

from account.serializers.customer_serizliers import (
    CustomAuthTokenSerializer,
    RegisterCustomerSerializer,
    CustomerResetPasswordSerializer,
    CustomerProfileSerializers,
    CustomerProfileUpdateSerializer,
)
from account.models import CustomerProfile, User
from account.permissions import IsAuthenticatedCustomer

from utils.loggers import general_logger, error_logger
from utils.emails import send_confirmation_email


class CustomerLoginView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    @extend_schema(responses=CustomAuthTokenSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        general_logger.info("a user login")

        return Response({"token": token.key, "email": user.email})


class ConfirmEmailAddress(APIView):
    def post(self,request,email,token):
        
        user = get_object_or_404(User,email=email,Token=token)
        if not user.is_verified:
            user.is_verified = True
            user.save()
        
        return Response({'msg':'your email confirmed successfully'})


class ResendEmailConfirm(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
    
    class OutPutSerilizer(serializers.Serializer):
        msg = serializers.CharField()

    @extend_schema(request=InputSerializer,responses=OutPutSerilizer)
    def post(self,request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user = get_object_or_404(User,email=email)
        if not user.is_verified:
            token = user.token
            send_confirmation_email(request,token,email)
            return Response(
            {"msg": f"Please check your email to confirm your email address"},
            status=status.HTTP_200_OK,
            )
        else:
            error_logger.error('email {email} is valid!')
            return Response(
            {"msg": f"Something is wrong. Please contact support for more information"},
            status=status.HTTP_400_BAD_REQUEST,
            )


class RegisterCustomerView(APIView):
    @extend_schema(request=RegisterCustomerSerializer)
    def post(self, request):
        serializer = RegisterCustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        token = random.randint(1,100000)
        User.objects.create_user(email=email, password=password, is_customer=True,is_verified=False,Token=token)
        send_confirmation_email(request,token,email)

        general_logger.info(f"user with {email} email address created")
        return Response(
            {"created": f"Your account has been created successfully. Please check your email to confirm your email address"},
            status=status.HTTP_201_CREATED,
        )


class CustomerResetPasswordView(APIView):
    permission_classes = [IsAuthenticatedCustomer]

    class OutputSerializer(serializers.Serializer):
        msg = serializers.CharField()

    @extend_schema(request=CustomerResetPasswordSerializer, responses=OutputSerializer)
    def patch(self, request):
        user = request.user
        serializer = CustomerResetPasswordSerializer(
            data=request.data, context={"user": user}
        )
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get("new_password")
        user.set_password(password)
        user.save()
        general_logger.info(f"user {user.email} update password")
        return Response(
            {"msg": "User password updated successfully"},
            status=status.HTTP_202_ACCEPTED,
        )


class CustomerForgetPasswordView(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=254)

    @staticmethod
    def send_forget_password_email(request, token, email):
        # Our Emails content
        host_name = request.get_host()
        send_mail(
            subject="forget password",
            message=f"http://{host_name}/forget/{token}/",
            from_email="admin@admin.com",
            recipient_list=[email],
            fail_silently=True,
        )
        general_logger.info(f"recovery email to {email} successfully")

    @extend_schema(request=InputSerializer)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token, created = Token.objects.get_or_create(user=user)
            self.send_forget_password_email(request, token, email)
            return Response(
                {"msg": "recovery email send successfully"}, status=status.HTTP_200_OK
            )
        else:
            error_logger.error(f"Email {email} Does Not exist")
            return Response(
                {"msg": "Email Does Not exist"}, status=status.HTTP_400_BAD_REQUEST
            )


class CustomerVerifyForgetPasswordView(APIView):
    class OutputSerializer(serializers.Serializer):
        token = serializers.CharField(read_only=True)
        msg = serializers.CharField(read_only=True)

    @extend_schema(responses=OutputSerializer)
    def post(self, request, token):
        if Token.objects.filter(key=token).exists():
            token = Token.objects.get(key=token)
            response = {"token": token.key, "msg": "success fully return"}
            general_logger.info(f"token {token} send to frontend")
            return Response(response, status=status.HTTP_200_OK)
        else:
            error_logger.error(f"token {token} does not exist.")
            return Response({"msg": "time error"}, status=status.HTTP_400_BAD_REQUEST)


class CustomerProfileView(APIView):
    permission_classes = [
        IsAuthenticatedCustomer,
    ]

    def get(self, request):
        profile = CustomerProfile.objects.get(user=request.user)
        serializer = CustomerProfileSerializers(profile)
        general_logger.info(f"profile {request.user.email} get")
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=CustomerProfileUpdateSerializer)
    def patch(self, request):
        serializer = CustomerProfileUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = CustomerProfile.objects.filter(user=request.user)
        profile.update(**serializer.validated_data)
        general_logger.info(f"profile {request.user.email} updated")
        return Response(
            {"msg": "profile update successfully"}, status=status.HTTP_202_ACCEPTED
        )
