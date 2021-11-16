from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

FOOD_TYPES = (
    ("drinks", "drinks"),
    ("main", "main"),
    ("side", "side"),
)

OPTIONS = (("ready", "ready"), ("not-ready", "not-ready"))


class RestaurantType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Type"
        verbose_name_plural = "Types"

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    class RestaurantObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status="ready")

    type = models.ForeignKey(RestaurantType, on_delete=models.PROTECT, default=1)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    phone_number = PhoneNumberField(null=True, blank=True)
    slug = models.SlugField(max_length=100, unique_for_date="updated")
    updated = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="restaurant")
    status = models.CharField(max_length=10, choices=OPTIONS, default="ready")
    objects = models.Manager()
    restaurantobjects = RestaurantObjects()

    class Meta:
        ordering = ("-updated",)

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=FOOD_TYPES)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.OneToOneField(
        Restaurant,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    food_items = models.ManyToManyField(FoodItem)

    def __str__(self):
        return self.restaurant
