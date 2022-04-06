from order.models import Order
from accounts.models import Client
from rest_framework import request, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .kafka_connection import conntect_kafka
from .serializers import (
    OrderMenuCheckSerializer,
    OrderMenuSerializer,
    OrderSerializer,
    validate_or_create_menu,
)

producer = conntect_kafka()


class OrderList(APIView):
    def get(self, request: request.Request, **kwargs) -> Response:
        order_id = kwargs.get("pk", None)
        user: Client = request.user

        if order_id is None:
            queryset = Order.objects.filter(user=user)
            order_serializer = OrderSerializer(queryset, many=True)
            return Response(order_serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                order = Order.objects.get(id=order_id)
                order_serializer = OrderSerializer(order)
                return Response(order_serializer.data, status=status.HTTP_200_OK)
            except Order.DoesNotExist:
                return Response(
                    "Order does not exist.", status=status.HTTP_400_BAD_REQUEST
                )

    def post(self, request: request.Request) -> Response:
        request.data["user"] = request.user.id
        order_serializer = OrderSerializer(data=request.data)
        order_menu_serializer = OrderMenuSerializer()
        order_menu_check_serializer = OrderMenuCheckSerializer()

        if order_serializer.is_valid():
            menus = request.data.get("menus", None)
            validate_or_create_menu(
                menus, order_menu_check_serializer
            )  # TODO: need to refactor
            order_res = order_serializer.save()
            validate_or_create_menu(menus, order_menu_serializer, order_res.id)

            producer.send("fast-food-order", order_serializer.data)

            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
