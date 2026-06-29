from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CoffeeProduct(models.Model):

    class RoastLevel(models.TextChoices):
        LIGHT = "light", "Light"
        MEDIUM = "medium", "Medium"
        DARK = "dark", "Dark"

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=200)

    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField()

    origin = models.CharField(max_length=100)

    roast_level = models.CharField(
        max_length=10,
        choices=RoastLevel.choices
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(default=0)

    image = models.ImageField(
        upload_to="coffee/",
        blank=True,
        null=True
    )

    available = models.BooleanField(default=True)

    featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class ProductImage(models.Model):

    product = models.ForeignKey(
        CoffeeProduct,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="coffee/gallery/"
    )

    def __str__(self):
        return self.product.name