from typing import Optional, Union

from home.models import FoodItem, Menu, Restaurant, RestaurantType
from order.models import Order, OrderMenu
from rest_framework import serializers

# Restaurant


class RestaurantTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantType
        fields = ("id", "name")


class RestaurantSerializer(serializers.ModelSerializer):
    # menus = serializers.ReadOnlyField()

    class Meta:
        model = Restaurant
        fields = ("id", "type_name", "name", "owner", "address", "zipcode", "phone_number", "menus")


class RestaurantFoodItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ("name", "description", "type")


class RestaurantMenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ("name", "price", "food_items")


# Order


class OrderMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMenu
        fields = ("id", "menu", "order", "quantity")


#  TODO: Need To Find Out How To Validate Fields Without Using Two Serializers


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
        fields = (
            "id",
            "username",
            "user",
            "user_zipcode",
            "created_on_str",
            "menus",
            "total_price",
            "restaurant",
            "restaurant_zipcode",
            "restaurant_name",
            "estimated_delivery_time",
            "delivery_time",
        )

    def validate(self, data):
        input_data = set(self.initial_data.keys())
        validation_data = {"menus", "user"}

        missing_values = validation_data - input_data

        if missing_values:
            raise serializers.ValidationError(f"Invalid data. Need {missing_values}.")

        return data


OrderMenuSerializers = Union[OrderMenuSerializer, OrderMenuCheckSerializer]


def validate_or_create_menu(menus, serializer: OrderMenuSerializers, order_id: Optional[str] = None) -> None:
    try:
        for menu in menus:
            if order_id:
                menu["order"] = order_id
                data = serializer.run_validation(menu)
                serializer.create(data)
            else:
                serializer.run_validation(menu)
    except (ValueError, KeyError, TypeError):
        raise serializers.ValidationError(f"Invalid menu data.")
