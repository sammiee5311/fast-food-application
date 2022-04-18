from functools import partial
from typing import Dict, Optional

from accounts.models import Client
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from home.models import FoodItem, Menu, Restaurant, RestaurantType
from rest_framework import request, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    RestaurantFoodItemsSerializer,
    RestaurantMenusSerializer,
    RestaurantSerializer,
    RestaurantTypesSerializer,
)


class RestaurantTypes(APIView):
    def get(self, request: request.Request, **kwargs) -> Response:
        queryset = RestaurantType.objects.all()
        try:
            restaurant_types_serializer = RestaurantTypesSerializer(queryset, many=True)

            return Response(restaurant_types_serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(restaurant_types_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestaurantMenus(APIView):
    """
    - example of request data -
    {
        "restaurant_id": "1",
        "menus": [
            {
                "name": "menu",
                "food_items": [
                    {
                        "name": "name",
                        "description": "food",
                        "type": "main"
                    }
                ],
                "price" : 12.99
            }
        ]
    }
    """

    def post(self, request: request.Request, **kwargs) -> Response:
        user: Client = request.user
        menus = request.data.get("menus", [])
        restaurant_id = request.data.get("restaurant_id", "")

        try:
            restaurant_menus = []
            restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

            for menu in menus:
                menu_price = menu["price"]
                menu_name = menu["name"]
                food_items = []

                for food_item in menu["food_items"]:
                    name = food_item["name"]
                    food_item, _ = FoodItem.objects.get_or_create(
                        name=name, description=food_item["description"], type=food_item["type"]
                    )
                    food_items.append(food_item.id)

                menu_serializer = RestaurantMenusSerializer(
                    data=dict(name=menu_name, price=menu_price, restaurant=restaurant_id, food_items=food_items)
                )

                if menu_serializer.is_valid():
                    menu_serializer.save()

                    restaurant_menus.append(menu_serializer.data)
                else:
                    return Response(menu_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            restaurant_serializer = RestaurantSerializer(restaurant, data={"menus": restaurant_menus}, partial=True)

            if restaurant_serializer.is_valid():
                restaurant_serializer.save()
                return Response(restaurant_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(restaurant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)


class RestaurantListByOwner(APIView):
    def get(self, request: request.Request, **kwargs) -> Response:
        owner: Client = request.user

        queryset: QuerySet = Restaurant.restaurantobjects.filter(owner=owner.id)

        try:
            restaurant_serializer = RestaurantSerializer(queryset, many=True)
            return Response(restaurant_serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(restaurant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestaurantList(APIView):
    def add_fields_if_not_in_request(self, restaruant: Restaurant, request: request.Request) -> Dict[str, str]:
        data = {}
        payload = request.data.keys()

        for key, val in request.data.items():
            data[key] = val
        if "owner" not in payload:
            data["owner"] = restaruant.owner.id
        if "address" not in payload:
            data["address"] = restaruant.address
        if "zipcode" not in payload:
            data["zipcode"] = restaruant.zipcode

        return data

    def post(self, request: request.Request) -> Response:
        user: Client = request.user
        request.data["owner"] = user.id
        restaurant_serializer = RestaurantSerializer(data=request.data)

        if restaurant_serializer.is_valid():
            restaurant_serializer.save()
            return Response(restaurant_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(restaurant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: request.Request, **kwargs) -> Response:
        restaurant_id = kwargs.get("pk", None)
        queryset: Optional[QuerySet]

        if restaurant_id is None:
            queryset = Restaurant.restaurantobjects.all()
        else:
            queryset = Restaurant.restaurantobjects.get(id=restaurant_id)

        try:
            restaurant_serializer = RestaurantSerializer(queryset, many=True)
            return Response(restaurant_serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(restaurant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: request.Request, **kwargs) -> Response:
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

    def patch(self, request: request.Request, **kwargs) -> Response:
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
