from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from home.models import FOOD_TYPES, OPTIONS, FoodItem, Menu, Restaurant, RestaurantType
from order.models import Order


class TestOrderModels(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="username", password="password")
        self.food_item = FoodItem.objects.create(id=0, name="burger", description="burger", type=FOOD_TYPES[1])
        self.restaraunt_type = RestaurantType.objects.create(id=0, name="hamburger")
        self.restaurant = Restaurant.objects.create(
            id=0,
            type=self.restaraunt_type,
            name="Happy burger",
            address="earth",
            phone_number="+1234567890",
            slug="happy-burger",
            updated=timezone.now(),
            owner=self.user,
            status=OPTIONS[0],
        )
        self.menu = Menu.objects.create(name="bulgogi-burger", price=5.99, restaurant=self.restaurant)
        self.menu.food_items.set([self.food_item])
        self.restaurant.menu.set([self.menu])
        self.order = Order.objects.create(id=1, user=self.user, price=self.menu.price, restaurant=self.restaurant)
        self.order.menu.set([self.menu])

    def test_name_of_order_model(self):
        self.assertEqual(str(self.order), f"{self.user} ordered food at {self.restaurant}.")
