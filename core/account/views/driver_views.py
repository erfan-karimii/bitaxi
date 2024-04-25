from rest_framework.views import APIView,Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class CustomeObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,'user_email':user.email})