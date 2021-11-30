from home.models import Restaurant
from order.models import Order
from rest_framework import serializers


class RestaurantSerializer(serializers.ModelSerializer):
    menus = serializers.ReadOnlyField()

    class Meta:
        model = Restaurant
        fields = ("id", "type_name", "name", "owner", "address", "phone_number", "menus")


class OrderSerializer(serializers.ModelSerializer):
    menus = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ("id", "username", "created_on_str", "menus", "total_price", "restaurant")
