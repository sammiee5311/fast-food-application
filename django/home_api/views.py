from home.models import Restaurant
from rest_framework import generics

from .serializers import RestaurantSerializer


class RestaurantList(generics.ListCreateAPIView):
    queryset = Restaurant.restaurantobjects.all()
    serializer_class = RestaurantSerializer


class RestaurantDetail(generics.RetrieveDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
