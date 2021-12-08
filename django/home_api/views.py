from typing import Dict

import rest_framework
from home.models import Restaurant
from order.models import Order
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    OrderMenuCheckSerializer,
    OrderMenuSerializer,
    OrderSerializer,
    RestaurantSerializer,
)


class RestaurantList(APIView):
    def add_fields_if_not_in_request(
        self, restaruant: Restaurant, request: rest_framework.request.Request
    ) -> Dict[str, str]:
        data = {}

        for key, val in request.data.items():
            data[key] = val
        if "owner" not in request.data.keys():
            data["owner"] = restaruant.owner.id
        if "address" not in request.data.keys():
            data["address"] = restaruant.address

        return data

    def post(self, request) -> Response:
        restaurant_serializer = RestaurantSerializer(data=request.data)

        if restaurant_serializer.is_valid():
            restaurant_serializer.save()
            return Response(restaurant_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(restaurant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, **kwargs) -> Response:
        restaurant_id = kwargs.get("pk", None)

        if restaurant_id is None:
            queryset = Restaurant.restaurantobjects.all()
            restaurant_serializer = RestaurantSerializer(queryset, many=True)
            return Response(restaurant_serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                restaurant_serializer = RestaurantSerializer(Restaurant.restaurantobjects.get(id=restaurant_id))
                return Response(restaurant_serializer.data, status=status.HTTP_200_OK)
            except Restaurant.DoesNotExist:
                return Response("Restaurant does not exist.", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs) -> Response:
        restaurant_id = kwargs.get("pk", None)

        if restaurant_id is None:
            return Response("Invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                restaruant = Restaurant.objects.get(id=restaurant_id)
                restaruant.delete()
                return Response("Restaurant is deleted successfully.", status=status.HTTP_200_OK)
            except Restaurant.DoesNotExist:
                return Response("Restaurant does not exist.", status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, **kwargs) -> Response:
        restaurant_id = kwargs.get("pk", None)

        if restaurant_id is None:
            return Response("Invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                restaruant = Restaurant.objects.get(id=restaurant_id)
                data = self.add_fields_if_not_in_request(restaruant, request)
                restaurant_serializer = RestaurantSerializer(restaruant, data=data)

                if restaurant_serializer.is_valid():
                    restaurant_serializer.save()
                    return Response(restaurant_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(restaurant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Restaurant.DoesNotExist:
                return Response("Restaurant does not exist.", status=status.HTTP_400_BAD_REQUEST)


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

        menus = request.data.get("menus", None)

        if order_serializer.is_valid():
            self.validate_or_create_menu(menus, order_menu_check_serializer)
            order_res = order_serializer.save()
            self.validate_or_create_menu(menus, order_menu_serializer, order_res.id)
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
