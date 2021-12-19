from accounts.models import Client
from django.db import models
from home.models import Menu, Restaurant


class Order(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="order", null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    menu = models.ManyToManyField(Menu, through="OrderMenu")
    estimated_delivery_time = models.IntegerField(
        null=True, blank=True
    )  # TODO: create delivery time model and make it foreign key ?
    delivery_time = models.IntegerField(
        null=True, blank=True
    )  # TODO: create a function that calculates time difference
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, null=False)

    class Meta:
        ordering = ("-created_on",)

    @property
    def menus(self):
        res = []
        for orders in self.ordermenu_set.all():
            res.append({"name": orders.menu.name, "price": orders.menu.price, "quantity": orders.quantity})
        return res

    @property
    def user_zipcode(self):
        return self.user.address.zipcode

    @property
    def restaurant_name(self):
        return self.restaurant.name

    @property
    def restaurant_zipcode(self):
        return self.restaurant.zipcode

    @property
    def total_price(self):
        res = 0
        for orders in self.ordermenu_set.all():
            res += orders.menu.price * orders.quantity
        return res

    @property
    def username(self):
        return self.user.username

    @property
    def created_on_str(self):
        return self.created_on.strftime(f"%Y-%m-%d %H:%M")

    def __str__(self):
        return f"{self.username} - {self.created_on_str}."


class OrderMenu(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=False)

    class Meta:
        verbose_name_plural = "Order menus"

    def __str__(self):
        return str(self.menu)
