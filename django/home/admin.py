from django.contrib import admin

from .models import FoodItem, Menu, Restaurant, Type

admin.site.register(Type)
admin.site.register(Restaurant)
admin.site.register(FoodItem)
admin.site.register(Menu)
