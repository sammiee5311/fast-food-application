import uuid

from accounts.models import Client
from django.urls import reverse
from django.utils import timezone
from order.models import Order, OrderMenu
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from restaurant.models import FOOD_TYPES, FoodItem, Menu, Restaurant, RestaurantType

TEST_UUID = uuid.uuid4()


def create_restaurant(user: Client, client: APIClient) -> Response:
    client.force_login(user)
    refresh = RefreshToken.for_user(user)
    restaraunt_type = RestaurantType.objects.create(id=1, name="hamburger")
    data = {
        "id": 1,
        "type": restaraunt_type.id,
        "name": "Happy burger",
        "address": "earth",
        "zipcode": "10013",
        "slug": "happy-burger",
        "updated": timezone.now(),
        "owner": user.id,
    }

    url = reverse("api:restaurant")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
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
    order = Order.objects.create(id=TEST_UUID, user=user, restaurant=restaurant)
    OrderMenu.objects.create(id=1, menu=menu, order=order, quantity=1)


class TestOwnerViewRestaurant(APITestCase):
    def setUp(self) -> None:
        self.user = Client.objects.create(id=0, email="test@test.com", username="username", password="password")
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}")

    def test_get_list_of_restaurants_by_owner(self) -> None:
        client = self.client
        client.force_login(self.user)
        create_restaurant(self.user, client)

        url = reverse("api:restaurant_by_owner")

        response = client.get(url, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["name"], "Happy burger")

    def test_add_menus_in_restaurant_success(self) -> None:
        client = self.client
        client.force_login(self.user)
        create_restaurant(self.user, client)

        restaurant = Restaurant.objects.get(id=1)
        create_menu(restaurant)

        data = {
            "restaurant_id": "1",
            "menus": [
                {
                    "name": "menu",
                    "food_items": [{"name": "name", "description": "food", "type": "main"}],
                    "price": 12.99,
                }
            ],
        }

        url = reverse("api:menu")
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 200)

    def test_add_menus_in_restaurant_fail(self) -> None:
        client = self.client
        client.force_login(self.user)
        create_restaurant(self.user, client)

        restaurant = Restaurant.objects.get(id=1)
        create_menu(restaurant)

        invalid_restaurant_id_data = {
            "restaurant_id": "2",
            "menus": [
                {
                    "name": "menu",
                    "food_items": [{"name": "name", "description": "food", "type": "main"}],
                    "price": 12.99,
                }
            ],
        }

        invalid_menu_serializer_data = {
            "restaurant_id": "1",
            "menus": [
                {
                    "name": "menu",
                    "food_items": [{"name": "name", "description": "food", "type": "main"}],
                    "price": "test",
                }
            ],
        }

        url = reverse("api:menu")
        invalid_id_response = self.client.post(url, invalid_restaurant_id_data, format="json")
        invalid_menu_response = self.client.post(url, invalid_menu_serializer_data, format="json")

        self.assertEqual(invalid_id_response.status_code, 400)
        self.assertEqual(invalid_menu_response.status_code, 400)


class TestViewRestaurant(APITestCase):
    def setUp(self) -> None:
        self.user = Client.objects.create(id=0, email="test@test.com", username="username", password="password")
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}")

    def test_get_restaurant_success(self) -> None:
        self.client.force_login(self.user)
        url = reverse("api:restaurant")
        response_get = self.client.get(url, format="json")

        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

    def test_get_particualr_restaurant(self) -> None:
        client = self.client
        client.force_login(self.user)
        create_restaurant(self.user, client)

        url = reverse("api:restaurant_detail", kwargs={"pk": 1})
        url_id_does_not_exist = reverse("api:restaurant_detail", kwargs={"pk": 123})
        response = client.get(url, format="json")
        response_id_does_not_exist = client.get(url_id_does_not_exist, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_id_does_not_exist.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_restaurant_failure(self) -> None:
        url = reverse("api:restaurant")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer fail")

        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_restaurant(self) -> None:
        client = self.client

        invalid_data_url = reverse("api:restaurant")
        invalid_data = {"phone_number": "Invalid data"}

        response = create_restaurant(self.user, client)
        response_invalid_data = client.post(invalid_data_url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["name"], "Happy burger")
        self.assertEqual(response_invalid_data.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_restaurant(self) -> None:
        client = self.client
        create_restaurant(self.user, client)

        data = {"name": "Super happy burger"}
        invalid_data = {"phone_number": "invalid phone number"}

        url = reverse("api:restaurant_detail", kwargs={"pk": 1})
        url_without_id = "http://localhost:8000/api/v0/restaurants/"
        url_id_does_not_exist = reverse("api:restaurant_detail", kwargs={"pk": 123})

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

        url = reverse("api:restaurant_detail", kwargs={"pk": 1})
        url_without_id = "http://localhost:8000/api/v0/restaurants/"
        url_id_does_not_exist = reverse("api:restaurant_detail", kwargs={"pk": 123})

        response = client.delete(url, format="json")
        response_without_id = client.delete(url_without_id, format="json")
        response_id_does_not_exist = client.delete(url_id_does_not_exist, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_without_id.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_id_does_not_exist.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_restaurants_types(self) -> None:
        client = self.client

        test_type = RestaurantType.objects.create(id=1, name="test")

        url = reverse("api:restaurant_type")

        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[-1]["name"], test_type.name)


class TestViewOrder(APITestCase):
    def setUp(self) -> None:
        self.user = Client.objects.create(username="username", password="password")
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}")

    def test_get_order_success(self) -> None:
        self.client.force_login(self.user)
        url = reverse("api:order")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order_failure(self) -> None:
        url = reverse("api:order")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer fail")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_particular_order(self) -> None:
        client = self.client
        create_restaurant(self.user, client)
        restaurant = Restaurant.objects.get(id=1)
        create_order(self.user, client, restaurant)

        url = reverse("api:order_detail", kwargs={"pk": TEST_UUID})
        url_id_does_not_exist = reverse("api:order_detail", kwargs={"pk": uuid.uuid4()})

        response = client.get(url, format="json")
        response_id_does_not_exist = client.get(url_id_does_not_exist, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["total_price"], 5.99)
        self.assertEqual(response_id_does_not_exist.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_order(self) -> None:
        client = self.client
        create_restaurant(self.user, client)
        restaurant = Restaurant.objects.get(id=1)
        menu = create_menu(restaurant)

        url = reverse("api:order")

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
            {
                "restaurant": restaurant.id,
                "user": self.user.id,
                "expect": status.HTTP_400_BAD_REQUEST,
            },
        ]

        for d in data:
            expect = d.pop("expect")
            response = client.post(url, d, format="json")
            self.assertEqual(response.status_code, expect)


class TestViewJWT(APITestCase):
    def setUp(self) -> None:
        self.user = Client.objects.create_user(
            id=0,
            email="test@test.com",
            username="username",
            password="password",
        )

    def test_get_tokens_and_refresh_token(self) -> None:
        tokens_url = reverse(
            "api:token_obtain_pair",
        )
        refresh_url = reverse(
            "api:token_refresh",
        )

        user_data = {"email": "test@test.com", "password": "password"}
        response = self.client.post(tokens_url, user_data, format="json")

        tokens = response.json()

        self.assertIn("refresh", tokens)

        refresh_data = {"refresh": tokens["refresh"]}
        response = self.client.post(refresh_url, refresh_data, format="json")

        self.assertIn("access", response.json())

    def test_validate_token_success(self) -> None:
        client = self.client
        refresh = RefreshToken.for_user(self.user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        url = reverse("api:token_validation")

        user_data = {"email": "test@test.com", "password": "password"}
        response = client.get(url, user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_validate_token_fail(self) -> None:

        url = reverse("api:token_validation")

        user_data = {"email": "test@test.com", "password": "password"}
        response = self.client.get(url, user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
