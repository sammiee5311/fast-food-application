from django.urls import path

from .views import RestaurantDetail, RestaurantList

app_name = "home_api"

urlpatterns = [
    path("restaurants/<int:pk>/", RestaurantDetail.as_view(), name="detailcreate"),
    path("restaurants/", RestaurantList.as_view(), name="listcreate"),
]
