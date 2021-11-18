from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from home.models import FOOD_TYPES, OPTIONS, FoodItem, Menu, Restaurant, RestaurantType


class TestHomeModels(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="username", password="password")
        self.food_item = FoodItem.objects.create(
            id=0, name="bulgogi-burger", description="bulgogi-burger", type=FOOD_TYPES[1]
        )
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
        self.menu = Menu.objects.create(restaurant=self.restaurant)

    def test_name_of_food_item_model(self):
        self.assertEqual(str(self.food_item), "bulgogi-burger")

    def test_name_of_restaurant_model(self):
        self.assertEqual(str(self.restaurant), "Happy burger")

    def test_name_of_restaruant_type_model(self):
        self.assertEqual(str(self.restaraunt_type), "hamburger")

    def test_name_of_last_menu_model(self):
        self.menu.food_items.set([self.food_item])
        self.assertEqual(str(self.menu), "bulgogi-burger")
