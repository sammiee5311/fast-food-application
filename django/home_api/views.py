from home.models import Restaurant
from rest_framework import generics
from rest_framework.serializers import Serializer

from .serializers import RestaurantSerializer

# class Restaurant(TemplateView):
#     model = Restaurant
#     template_name = 'name'

#     def get_context_data
#         context = super(Menu, self).get_context_data(**kwargs)
#         restaurant = Restaurant.objects.get(name='McDonalds')
#         context['restaurant'] = Restaurant.objects.get(name='McDonalds')
#         context['menu'] = Menu.objects.get(restaurant=restaurant)
#         return context


class RestaurantList(generics.ListCreateAPIView):
    queryset = Restaurant.restaurantobjects.all()
    serializer_class = RestaurantSerializer


class RestaurantDetail(generics.RetrieveDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
