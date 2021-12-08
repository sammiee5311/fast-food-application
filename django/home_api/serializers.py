from home.models import Restaurant
from order.models import Order, OrderMenu
from rest_framework import serializers


class RestaurantSerializer(serializers.ModelSerializer):
    menus = serializers.ReadOnlyField()

    class Meta:
        model = Restaurant
        fields = ("id", "type_name", "name", "owner", "address", "phone_number", "menus")


class OrderMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMenu
        fields = ("id", "menu", "order", "quantity")


#  Need To Find Out How To Validate Fields Without Using Two Serializers


class OrderMenuCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMenu
        fields = ("id", "menu", "quantity")

    def validate_quantity(self, data):
        if data <= 0:
            raise serializers.ValidationError(f"Invalid data. Menu quantity must be greather than 0.")

        return data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "username", "user", "created_on_str", "menus", "total_price", "restaurant")

    def validate(self, data):
        input_data = set(self.initial_data.keys())
        validation_data = {"menus", "user"}

        missing_values = validation_data - input_data

        if missing_values:
            raise serializers.ValidationError(f"Invalid data. Need {missing_values}.")

        return data
