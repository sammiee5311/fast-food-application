from home.models import Restaurant
from rest_framework import serializers


class RestaurantSerializer(serializers.ModelSerializer):
    menus = serializers.ReadOnlyField()

    class Meta:
        model = Restaurant
        fields = ("id", "type", "name", "owner", "address", "phone_number", "status", "menus")
