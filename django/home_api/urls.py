from django.urls import path

from .views import RestaurantList

app_name = "home_api"

urlpatterns = [
    path("restaurants/<int:pk>/", RestaurantList.as_view(), name="detailcreate"),
    path("restaurants/", RestaurantList.as_view(), name="listcreate"),
]
