from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CUSTOMER = "customer"
    ADMIN = "admin"

    ROLE_CHOICES = [
        (CUSTOMER, "Customer"),
        (ADMIN, "Admin"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=CUSTOMER
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username