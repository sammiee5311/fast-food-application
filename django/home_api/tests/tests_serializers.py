from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from home.models import RestaurantType
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

    def create_restaurant(self, client):
        client.force_login(self.user)
        restaraunt_type = RestaurantType.objects.create(id=1, name="hamburger")
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

    def test_update_restaurant(self):
        client = self.client
        self.create_restaurant(client)

        data = {"name": "Super happy burger"}

        url = reverse("home_api:detailcreate", kwargs={"pk": 1})
        response = client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Super happy burger")

    def test_delete_restaurant(self):
        client = self.client
        self.create_restaurant(client)

        url = reverse("home_api:detailcreate", kwargs={"pk": 1})
        response = client.delete(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
