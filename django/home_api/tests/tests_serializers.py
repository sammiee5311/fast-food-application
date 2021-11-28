import json

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from home.models import FOOD_TYPES, FoodItem, Menu, Restaurant, RestaurantType
from order.models import Order
from rest_framework import status
from rest_framework.test import APITestCase


def create_restaurant(user, client):
    client.force_login(user)
    restaraunt_type = RestaurantType.objects.create(id=1, name="hamburger")
    data = {
        "type": restaraunt_type.id,
        "name": "Happy burger",
        "address": "earth",
        "slug": "happy-burger",
        "updated": timezone.now(),
        "owner": user.id,
    }

    url = reverse("home_api:restaurant")
    response = client.post(url, data, format="json")

    return response


def create_menu(restaurant):
    food_item = FoodItem.objects.create(id=1, name="burger", description="burger", type=FOOD_TYPES[1])
    menu = Menu.objects.create(name="bulgogi-burger", price=5.99, restaurant=restaurant)
    menu.food_items.set([food_item])
    restaurant.menu.set([menu])

    return menu


def create_order(user, client, restaurant):
    client.force_login(user)
    menu = create_menu(restaurant)
    order = Order.objects.create(id=1, user=user, price=menu.price, restaurant=restaurant)
    order.menu.set([menu])


class TestViewRestaurant(APITestCase):
    def setUp(self):
        self.user = User.objects.create(id=0, username="username", password="password")

    def test_view_restaurant_success(self):
        self.client.force_login(self.user)
        url = reverse("home_api:restaurant")
        response_get = self.client.get(url, format="json")

        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

    def test_view_restaurant_failure(self):
        url = reverse("home_api:restaurant")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_restaurant(self):
        client = self.client
        response = create_restaurant(self.user, client)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["name"], "Happy burger")

    def test_update_restaurant(self):
        client = self.client
        create_restaurant(self.user, client)

        data = {"name": "Super happy burger"}

        url = reverse("home_api:restaurant_detail", kwargs={"pk": 1})
        response = client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Super happy burger")

    def test_delete_restaurant(self):
        client = self.client
        create_restaurant(self.user, client)

        url = reverse("home_api:restaurant_detail", kwargs={"pk": 1})
        response = client.delete(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestViewOrder(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="username", password="password")

    def test_view_order_success(self):
        self.client.force_login(self.user)
        url = reverse("home_api:order")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_order_failure(self):
        url = reverse("home_api:order")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_particular_order(self):
        client = self.client
        create_restaurant(self.user, client)
        restaurant = Restaurant.objects.get(id=1)
        create_order(self.user, client, restaurant)

        url = reverse("home_api:order_detail", kwargs={"pk": 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["total_price"], 5.99)
