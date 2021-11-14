from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Type(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Type"
        verbose_name_plural = "Types"

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    class RestaurantObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter("ready")

    options = (("ready", "Ready"), ("not-ready", "Not-Ready"))

    type = models.ForeignKey(Type, on_delete=models.PROTECT, default=1)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    phone_number = PhoneNumberField(null=True, blank=True)
    slug = models.SlugField(max_length=100, unique_for_date="updated")
    updated = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="restaurant")
    status = models.CharField(max_length=10, choices=options, default="ready")
    objects = models.Manager()
    restaurantobjects = RestaurantObjects()

    class Meta:
        ordering = ("-updated",)

    def __str__(self):
        return self.name
