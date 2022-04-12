from typing import Dict

from accounts.models import Client
from home.models import Restaurant, RestaurantType
from rest_framework import request, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RestaurantSerializer, RestaurantTypesSerializer


class RestaurantTypes(APIView):
    def get(self, request: request.Request, **kwargs) -> Response:
        queryset = RestaurantType.objects.all()
        try:
            restaurant_types_serializer = RestaurantTypesSerializer(queryset, many=True)

            return Response(restaurant_types_serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(restaurant_types_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        request.data["owner"] = user
        restaurant_serializer = RestaurantSerializer(data=request.data)

        if restaurant_serializer.is_valid():
            restaurant_serializer.save()
            return Response(restaurant_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(restaurant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: request.Request, **kwargs) -> Response:
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
