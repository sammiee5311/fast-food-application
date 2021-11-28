from django.urls import path

from .views import OrderList, RestaurantList

app_name = "home_api"

urlpatterns = [
    path("restaurants/<int:pk>/", RestaurantList.as_view(), name="restaurant_detail"),
    path("restaurants/", RestaurantList.as_view(), name="restaurant"),
    path("orders/<int:pk>/", OrderList.as_view(), name="order_detail"),
    path("orders/", OrderList.as_view(), name="order"),
]
