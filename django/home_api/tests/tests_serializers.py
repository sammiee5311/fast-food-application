from accounts.models import Client
from django.urls import reverse
from django.utils import timezone
from home.models import FOOD_TYPES, FoodItem, Menu, Restaurant, RestaurantType
from order.models import Order, OrderMenu
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase


def create_restaurant(user: Client, client: APIClient) -> Response:
    client.force_login(user)
    restaraunt_type = RestaurantType.objects.create(id=1, name="hamburger")
    data = {
        "type": restaraunt_type.id,
        "name": "Happy burger",
        "address": "earth",
        "zipcode": 12345,
        "slug": "happy-burger",
        "updated": timezone.now(),
        "owner": user.id,
    }

    url = reverse("home_api:restaurant")
    response = client.post(url, data, format="json")

    return response


def create_menu(restaurant: Restaurant) -> Menu:
    food_item = FoodItem.objects.create(id=1, name="burger", description="burger", type=FOOD_TYPES[1])
    menu = Menu.objects.create(name="bulgogi-burger", price=5.99, restaurant=restaurant)
    menu.food_items.set([food_item])
    restaurant.menu.set([menu])

    return menu


def create_order(user, client: APIClient, restaurant: Restaurant) -> None:
    client.force_login(user)
    menu = create_menu(restaurant)
    order = Order.objects.create(id=1, user=user, restaurant=restaurant)
    OrderMenu.objects.create(id=1, menu=menu, order=order, quantity=1)


class TestViewRestaurant(APITestCase):
    def setUp(self) -> None:
        self.user = Client.objects.create(id=0, email="test@test.com", username="username", password="password")

    def test_get_restaurant_success(self) -> None:
        self.client.force_login(self.user)
        url = reverse("home_api:restaurant")
        response_get = self.client.get(url, format="json")

        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

    def test_get_particualr_restaurant(self) -> None:
        client = self.client
        client.force_login(self.user)
        create_restaurant(self.user, client)

        url = reverse("home_api:restaurant_detail", kwargs={"pk": 1})
        url_id_does_not_exist = reverse("home_api:restaurant_detail", kwargs={"pk": 123})
        response = client.get(url, format="json")
        response_id_does_not_exist = client.get(url_id_does_not_exist, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_id_does_not_exist.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_restaurant_failure(self) -> None:
        url = reverse("home_api:restaurant")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_restaurant(self) -> None:
        client = self.client

        url_invalid_data = reverse("home_api:restaurant")
        invalid_data = {"phone_number": "Invalid data"}

        response = create_restaurant(self.user, client)
        response_invalid_data = client.post(url_invalid_data, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["name"], "Happy burger")
        self.assertEqual(response_invalid_data.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_restaurant(self) -> None:
        client = self.client
        create_restaurant(self.user, client)

        data = {"name": "Super happy burger"}
        invalid_data = {"phone_number": "invalid phone number"}

        url = reverse("home_api:restaurant_detail", kwargs={"pk": 1})
        url_without_id = "http://localhost:8000/api/restaurants/"
        url_id_does_not_exist = reverse("home_api:restaurant_detail", kwargs={"pk": 123})

        response = client.patch(url, data, format="json")
        response_without_id = client.patch(url_without_id, data, format="json")
        response_invalid_data = client.patch(url, invalid_data, format="json")
        response_id_does_not_exist = client.patch(url_id_does_not_exist, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Super happy burger")
        self.assertEqual(response_without_id.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_invalid_data.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_id_does_not_exist.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_restaurant(self) -> None:
        client = self.client
        create_restaurant(self.user, client)

        url = reverse("home_api:restaurant_detail", kwargs={"pk": 1})
        url_without_id = "http://localhost:8000/api/restaurants/"
        url_id_does_not_exist = reverse("home_api:restaurant_detail", kwargs={"pk": 123})

        response = client.delete(url, format="json")
        response_without_id = client.delete(url_without_id, format="json")
        response_id_does_not_exist = client.delete(url_id_does_not_exist, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_without_id.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_id_does_not_exist.status_code, status.HTTP_400_BAD_REQUEST)


class TestViewOrder(APITestCase):
    def setUp(self) -> None:
        self.user = Client.objects.create(username="username", password="password")

    def test_get_order_success(self) -> None:
        self.client.force_login(self.user)
        url = reverse("home_api:order")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order_failure(self) -> None:
        url = reverse("home_api:order")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_particular_order(self) -> None:
        client = self.client
        create_restaurant(self.user, client)
        restaurant = Restaurant.objects.get(id=1)
        create_order(self.user, client, restaurant)

        url = reverse("home_api:order_detail", kwargs={"pk": 1})
        url_id_does_not_exist = reverse("home_api:order_detail", kwargs={"pk": 123})

        response = client.get(url, format="json")
        response_id_does_not_exist = client.get(url_id_does_not_exist, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["total_price"], 5.99)
        self.assertEqual(response_id_does_not_exist.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_order(self) -> None:
        client = self.client
        create_restaurant(self.user, client)
        restaurant = Restaurant.objects.get(id=1)
        create_menu(restaurant)
        menu = Menu.objects.get(id=1)

        url = reverse("home_api:order")

        data = [
            {
                "restaurant": restaurant.id,
                "user": self.user.id,
                "menus": [{"menu": menu.id, "quantity": 1}],
                "expect": status.HTTP_201_CREATED,
            },
            {
                "restaurant": restaurant.id,
                "user": self.user.id,
                "menus": [{"menu": menu.id, "quantity": -1}],
                "expect": status.HTTP_400_BAD_REQUEST,
            },
            {"restaurant": restaurant.id, "user": self.user.id, "expect": status.HTTP_400_BAD_REQUEST},
        ]

        for d in data:
            expect = d.pop("expect")
            response = client.post(url, d, format="json")
            self.assertEqual(response.status_code, expect)
