from django.contrib import admin

from .models import FoodItem, Menu, Restaurant, RestaurantType

admin.site.register(RestaurantType)
admin.site.register(Restaurant)
admin.site.register(FoodItem)
admin.site.register(Menu)
