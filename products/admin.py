from django.contrib import admin
from .models import Category, CoffeeProduct, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(CoffeeProduct)
class CoffeeProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "price",
        "stock",
        "featured",
        "available",
    )

    list_filter = (
        "category",
        "featured",
        "available",
    )

    search_fields = (
        "name",
        "origin",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    inlines = [
        ProductImageInline
    ]