from accounts.models import Client
from django.test import TestCase
from django.utils import timezone
from home.models import FOOD_TYPES, OPTIONS, FoodItem, Menu, Restaurant, RestaurantType


class TestRestaurantsModels(TestCase):
    def setUp(self):
        self.user = Client.objects.create(username="username", email="test@test.com", password="password")
        self.food_item = FoodItem.objects.create(id=0, name="burger", description="burger", type=FOOD_TYPES[1])
        self.restaraunt_type = RestaurantType.objects.create(id=0, name="hamburger")
        self.restaurant = Restaurant.objects.create(
            id=0,
            type=self.restaraunt_type,
            name="Happy burger",
            address="earth",
            zipcode="10013",
            phone_number="+1234567890",
            slug="happy-burger",
            updated=timezone.now(),
            owner=self.user,
            status=OPTIONS[0],
        )
        self.menu1 = Menu.objects.create(name="bulgogi-burger", price=5.99, restaurant=self.restaurant)
        self.menu2 = Menu.objects.create(name="cheese-burger", price=4.99, restaurant=self.restaurant)
        self.menu1.food_items.set([self.food_item])
        self.menu2.food_items.set([self.food_item])
        self.restaurant.menu.set([self.menu1, self.menu2])

    def test_name_of_food_item_model(self):
        self.assertEqual(str(self.food_item), "burger")

    def test_name_of_restaurant_model(self):
        self.assertEqual(str(self.restaurant), "Happy burger")

    def test_name_of_restaruant_type_model(self):
        self.assertEqual(str(self.restaraunt_type), "hamburger")

    def test_name_of_last_menu_model(self):
        self.assertEqual(str(self.menu1), "bulgogi-burger")
        self.assertEqual(str(self.menu2), "cheese-burger")

    def test_list_of_menus(self):
        menus = [
            {"menu_id": self.menu1.id, "name": "bulgogi-burger", "price": 5.99},
            {"menu_id": self.menu2.id, "name": "cheese-burger", "price": 4.99},
        ]
        self.assertEqual(self.restaurant.menus, menus)
