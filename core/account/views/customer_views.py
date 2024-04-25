from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from account.serializers.customer_serizliers import CustomAuthTokenSerializer

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