from rest_framework import request, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    ValidationError,
)
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class MyTokenValidation(APIView):
    def get(self, request: request.Request, **kwargs):
        try:
            token = request.META.get("HTTP_AUTHORIZATION", " ").split(" ")[1]
            valid_data = TokenBackend(algorithm="HS256").decode(token, verify=False)

            return Response(valid_data, status=status.HTTP_401_UNAUTHORIZED)

        except ValidationError as err:
            return Response(
                f"Token is invalid. err: {err}", status=status.HTTP_401_UNAUTHORIZED
            )
