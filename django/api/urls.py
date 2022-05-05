from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .jwt_views import MyTokenObtainPairView, MyTokenValidation
from .order_views import OrderList
from .restaruant_views import RestaurantList
from .restaurant_owner_views import (
    RestaurantListByOwner,
    RestaurantMenus,
    RestaurantTypes,
)

app_name = "api"

urlpatterns = [
    path("restaurants/<int:pk>/", RestaurantList.as_view(), name="restaurant_detail"),
    path("restaurants/", RestaurantList.as_view(), name="restaurant"),
    path(
        "restaurantsbyowner/",
        RestaurantListByOwner.as_view(),
        name="restaurant_by_owner",
    ),
    path("restaurantstypes/", RestaurantTypes.as_view(), name="restaurant_type"),
    path("orders/<str:pk>/", OrderList.as_view(), name="order_detail"),
    path("orders/", OrderList.as_view(), name="order"),
    path("menus/", RestaurantMenus.as_view(), name="menu"),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/validation/", MyTokenValidation.as_view(), name="token_validation"),
]
