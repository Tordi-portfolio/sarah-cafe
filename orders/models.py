from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from products.models import CoffeeProduct


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        CoffeeProduct,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name
    

from decimal import Decimal


class Order(models.Model):

    STATUS_CHOICES = [

        ("Pending", "Pending"),

        ("Approved", "Approved"),

        ("Rejected", "Rejected"),

        ("Cancelled", "Cancelled"),

        ("Delivered", "Delivered"),

    ]

    PAYMENT_CHOICES = [

        ("Pending", "Pending"),

        ("Cancelled", "Cancelled"),

        ("Paid", "Paid"),

    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    full_name = models.CharField(max_length=200)

    email = models.EmailField()

    phone = models.CharField(max_length=30)

    address = models.TextField()

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    zip_code = models.CharField(max_length=30)

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="Pending"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return f"Order #{self.id}"
    

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        CoffeeProduct,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):

        return self.product.name