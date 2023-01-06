from core.tracing import tracer
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
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
            traceparent = request.headers.get_all("traceparent")
            carrier = {"traceparent": traceparent[0]}
            ctx = TraceContextTextMapPropagator().extract(carrier)
        except LookupError:
            ctx = {}

        try:
            with tracer.start_as_current_span("get-token", context=ctx) as span:
                token = request.META.get("HTTP_AUTHORIZATION", " ").split(" ")[1]
                valid_data = TokenBackend(algorithm="HS256").decode(token, verify=False)

                if span.is_recording():
                    span.set_attribute("request.user", request.user)

                return Response(valid_data, status=status.HTTP_200_OK)

        except ValidationError as err:
            with tracer.start_as_current_span("get-token", context=ctx) as span:
                if span.is_recording():
                    span.set_attribute("request.user", request.user)
                    span.set_status(trace.Status(trace.StatusCode.ERROR, str(err)))

                return Response(f"Token is invalid. err: {err}", status=status.HTTP_401_UNAUTHORIZED)
