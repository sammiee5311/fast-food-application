from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models


class EmailError(ValidationError):
    def __init__(self, message="You must type an email address"):
        self.message = message
        super().__init__(self.message)


class Address(models.Model):
    street = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=5, blank=False)
    city = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.zipcode


class CustomAccountManager(BaseUserManager):
    def _validate_email(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise EmailError("Email is invalid")

    def create_superuser(self, email, username, password, **fields):
        fields.setdefault("is_staff", True)
        fields.setdefault("is_superuser", True)
        fields.setdefault("is_active", True)

        if email:
            email = self.normalize_email(email)
            self._validate_email(email)
        else:
            raise EmailError()

        return self.create_user(email, username, password, **fields)

    def create_user(self, email, username, password, **fields):
        if email:
            email = self.normalize_email(email)
            self._validate_email(email)
        else:
            raise EmailError()

        user = self.model(email=email, username=username, **fields)
        user.set_password(password)
        user.save()

        return user


class Client(AbstractUser):
    email = models.EmailField("email address", unique=True)
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
