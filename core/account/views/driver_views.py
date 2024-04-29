from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from account.serializers.driver_serializers import (
    InputRegisterSerializers,CustomAuthTokenSerializer,ResetPasswordSerializer,
    ForgetPasswordSerializer,DriverProfileSerializers
    )
from rest_framework import status,serializers
from drf_spectacular.utils import extend_schema
from account.models import User,DriverProfile
from account.permissions import IsDriver

class DriverSignUP(APIView):
    class OutputRegisterSerializers(serializers.Serializer):
        email = serializers.EmailField(read_only=True)
        message = serializers.CharField(read_only=True)

    @extend_schema(request=InputRegisterSerializers,responses=OutputRegisterSerializers)
    def post(self, request):
        serializers = InputRegisterSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            response = {"email":serializers.data['email'],"message":"اکانت شما با موفقیت ساخته شد",}
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors)





class DriverLogin(ObtainAuthToken):
    @extend_schema(request=CustomAuthTokenSerializer,responses=CustomAuthTokenSerializer)
    def post(self, request, *args, **kwargs):
        serializer = CustomAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,'email':user.email})
    

class ResetPassword(APIView):

    def put(self,request):
        serializer = ResetPasswordSerializer(data=request.data,context ={'request':request})
        if serializer.is_valid():
            serializer.update(serializer.validated_data)
            return Response({"msg":"Your Password Changed"},status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,)


class ForgetPassword(APIView):

    @staticmethod
    def send_email(token):
        # Our Emails content
        print(f'127.0.0.1:8000/custom/{token}/')
    
    def post(self,request):
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                token, created = Token.objects.get_or_create(user=user)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({"msg":"Email Does Not exist"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors)


class VerifyForgetPassword(APIView):
    class SerializerVerifyForgetPasswordOutPut(serializers.Serializer):
        token = serializers.CharField(read_only=True)
        msg = serializers.CharField(read_only=True)
    def post(self,request,token):
        if Token.objects.filter(key=token).exists():
            token = Token.objects.get(key=token)
            response = {
                'token':token.key,
                'msg':"success fully return"
            }
            return Response(response,status=status.HTTP_200_OK)
        else:
            return Response({"msg":"time error"},status=status.HTTP_400_BAD_REQUEST)
        

        
    

class DriverProfileView(APIView):
    permission_classes=[IsDriver,]
    def get(self,request):
        profile = DriverProfile.objects.get(user=request.user)
        serializer = DriverProfileSerializers(profile)
        return Response(serializer.data,status=status.HTTP_200_OK)


    def put(self,request):
        profile = DriverProfile.objects.get(user=request.user)
        serializer = DriverProfileSerializers(profile,data=request.data)
        if serializer.is_valid():
            serializer.update(instance=profile,validated_data=serializer.validated_data)
            return Response({"msg":"your update success"},status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)