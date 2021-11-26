from typing import Dict

import rest_framework
from home.models import Restaurant
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RestaurantSerializer


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
            restaurant_serializer = RestaurantSerializer(Restaurant.restaurantobjects.get(id=restaurant_id))
            return Response(restaurant_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, **kwargs) -> Response:
        restaurant_id = kwargs.get("pk", None)

        if restaurant_id is None:
            return Response("Invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            restaruant = Restaurant.objects.get(id=restaurant_id)
            restaruant.delete()
            return Response("Restaraunt is deleted successfully.", status=status.HTTP_200_OK)

    def patch(self, request, **kwargs) -> Response:
        restaurant_id = kwargs.get("pk", None)

        if restaurant_id is None:
            return Response("Invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            restaruant = Restaurant.objects.get(id=restaurant_id)

            data = self.add_fields_if_not_in_request(restaruant, request)

            restaurant_serializer = RestaurantSerializer(restaruant, data=data)

            if restaurant_serializer.is_valid():
                restaurant_serializer.save()
                return Response(restaurant_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(restaurant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
