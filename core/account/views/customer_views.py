from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import extend_schema

from account.serializers.customer_serizliers import CustomAuthTokenSerializer , RegisterCustomerSerializer
from account.models import CustomerProfile , User

class CustomCustomerAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    
    @extend_schema(responses=CustomAuthTokenSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'email': user.email
        })


class RegisterCustomerView(APIView):
    @extend_schema(request=RegisterCustomerSerializer)
    def post(self,request):
        serializer =  RegisterCustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = User.objects.create_user(email=email,password=password,is_driver=True)
        CustomerProfile.objects.create(user=user,first_name='',last_name='')
        
        # serializer.validated_data.update({'is_driver':True})
        # serializer.save()
        return Response({'created':f'user with {email} email address created'},status=status.HTTP_201_CREATED)
        