import json
import socket

from kafka import KafkaProducer
from order.models import Order
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import OrderMenuCheckSerializer, OrderMenuSerializer, OrderSerializer

IP_ADDRESS = socket.gethostbyname(socket.gethostname())


def json_serializer(data):
    return json.dumps(data).encode("utf-8")


producer = KafkaProducer(
    security_protocol="PLAINTEXT",
    bootstrap_servers=[f"{IP_ADDRESS}:9092"],
    value_serializer=json_serializer,
    retries=10,
    retry_backoff_ms=1000,
)


class OrderList(APIView):
    def validate_or_create_menu(self, menus, serializer, order_id=None) -> None:
        for menu in menus:
            if order_id:
                menu["order"] = order_id
                data = serializer.run_validation(menu)
                serializer.create(data)
            else:
                serializer.run_validation(menu)

    def get(self, request, **kwargs) -> Response:
        order_id = kwargs.get("pk", None)

        if order_id is None:
            queryset = Order.objects.all()
            order_serializer = OrderSerializer(queryset, many=True)
            return Response(order_serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                order = Order.objects.get(id=order_id)
                order_serializer = OrderSerializer(order)
                return Response(order_serializer.data, status=status.HTTP_200_OK)
            except Order.DoesNotExist:
                return Response("Order does not exist.", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request) -> Response:
        order_serializer = OrderSerializer(data=request.data)
        order_menu_serializer = OrderMenuSerializer()
        order_menu_check_serializer = OrderMenuCheckSerializer()
        if order_serializer.is_valid():
            menus = request.data.get("menus", None)
            self.validate_or_create_menu(menus, order_menu_check_serializer)
            order_res = order_serializer.save()
            self.validate_or_create_menu(menus, order_menu_serializer, order_res.id)

            producer.send("fast-food-order", order_serializer.data)

            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
