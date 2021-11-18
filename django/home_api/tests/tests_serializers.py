from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from home.models import FOOD_TYPES, OPTIONS, FoodItem, Menu, Restaurant, RestaurantType
from rest_framework import status
from rest_framework.test import APITestCase


class TestViewRestaurant(APITestCase):
    def setUp(self):
        self.user = User.objects.create(id=0, username="username", password="password")

    def test_view_restaurant_success(self):
        self.client.force_login(self.user)
        url = reverse("home_api:listcreate")
        response_get = self.client.get(url, format="json")

        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

    def test_view_restaurant_failure(self):
        url = reverse("home_api:listcreate")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_restaurant(self):
        self.client.force_login(self.user)
        restaraunt_type = RestaurantType.objects.create(id=0, name="hamburger")
        data = {
            "type": restaraunt_type.id,
            "name": "Happy burger",
            "address": "earth",
            "slug": "happy-burger",
            "updated": timezone.now(),
            "owner": self.user.id,
        }

        url = reverse("home_api:listcreate")
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["name"], "Happy burger")
