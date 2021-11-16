from home.models import Restaurant
from rest_framework import serializers


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("type", "name", "owner", "address", "phone_number", "status")
