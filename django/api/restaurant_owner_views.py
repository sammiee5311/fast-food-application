from accounts.models import Client
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from home.models import FoodItem, Restaurant, RestaurantType
from rest_framework import request, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
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
            return Response(
                restaurant_types_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


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
                        name=name,
                        description=food_item["description"],
                        type=food_item["type"],
                    )
                    food_items.append(food_item.id)

                menu_serializer = RestaurantMenusSerializer(
                    data=dict(
                        name=menu_name,
                        price=menu_price,
                        restaurant=restaurant_id,
                        food_items=food_items,
                    )
                )

                if menu_serializer.is_valid():
                    menu_serializer.save()

                    restaurant_menus.append(menu_serializer.data)
                else:
                    return Response(
                        menu_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            restaurant_serializer = RestaurantSerializer(
                restaurant, data={"menus": restaurant_menus}, partial=True
            )

            if restaurant_serializer.is_valid():
                restaurant_serializer.save()
                return Response(restaurant_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    restaurant_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
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
            return Response(
                restaurant_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
