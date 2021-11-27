from django.contrib.auth.models import User
from django.db import models
from home.models import Menu, Restaurant


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    menu = models.ManyToManyField(Menu, related_name="order", blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)

    class Meta:
        ordering = ("-created_on",)

    @property
    def menus(self):
        res = []
        for menu in self.menu.all():
            res.append({"name": menu.name, "price": menu.price})
        return res

    @property
    def total_price(self):
        res = 0
        for menu in self.menu.all():
            res += menu.price
        return res

    def __str__(self):
        return f"{self.user} ordered food at {self.restaurant}."
