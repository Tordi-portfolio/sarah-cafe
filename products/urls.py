from django.urls import path
from . import views

urlpatterns = [
    path("", views.shop, name="shop"),
    path("<slug:slug>/", views.product_detail, name="product_detail"),

    # Products
    path("products/", views.product_list, name="dashboard_products"),
    path("products/add/", views.add_product, name="add_product"),
    path("products/edit/<int:id>/", views.edit_product, name="edit_product"),
    path("products/delete/<int:id>/", views.delete_product, name="delete_product"),

    # Categories
    path("categories/", views.category_list, name="dashboard_categories"),
]