from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .jwt_views import MyTokenObtainPairView
from .order_views import OrderList
from .restaruant_views import RestaurantList, RestaurantTypes

app_name = "home_api"

urlpatterns = [
    path("restaurants/<int:pk>/", RestaurantList.as_view(), name="restaurant_detail"),
    path("restaurants/", RestaurantList.as_view(), name="restaurant"),
    path("restaurants/", RestaurantList.as_view(), name="restaurant"),
    path("restauratnstypes/", RestaurantTypes.as_view(), name="restaurant_type"),
    path("orders/<str:pk>/", OrderList.as_view(), name="order_detail"),
    path("orders/", OrderList.as_view(), name="order"),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
