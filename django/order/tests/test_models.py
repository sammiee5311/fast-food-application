import uuid

from accounts.models import Client
from django.test import TestCase
from django.utils import timezone
from restaurant.models import (
    FOOD_TYPES,
    OPTIONS,
    FoodItem,
    Menu,
    Restaurant,
    RestaurantType,
)
from order.models import Order, OrderMenu


class TestOrderModels(TestCase):
    def setUp(self):
        self.user = Client.objects.create(
            username="username", email="test@test.com", password="password"
        )
        self.food_item = FoodItem.objects.create(
            id=0, name="burger", description="burger", type=FOOD_TYPES[1]
        )
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
        self.menu = Menu.objects.create(
            name="bulgogi-burger", price=5.99, restaurant=self.restaurant
        )
        self.menu.food_items.set([self.food_item])
        self.restaurant.menu.set([self.menu])
        self.order = Order.objects.create(
            id=uuid.uuid4(), user=self.user, restaurant=self.restaurant
        )
        self.order_menu1 = OrderMenu.objects.create(
            id=1, menu=self.menu, order=self.order, quantity=1
        )
        self.order_menu2 = OrderMenu.objects.create(
            id=2, menu=self.menu, order=self.order, quantity=2
        )

    def test_name_of_order_model(self):
        self.assertEqual(str(self.order).split("-")[0].strip(), "username")

    def test_name_of_order_menu_model(self):
        self.assertEqual(str(self.order_menu1), "bulgogi-burger")

    def test_total_price_of_order(self):
        total_price = 0

        for order_menu in self.order.ordermenu_set.all():
            total_price += order_menu.menu.price * order_menu.quantity

        self.assertEqual(total_price, 5.99 * 3)
