from django.urls import path
from . import views

urlpatterns = [

    path("", views.customer_dashboard, name="dashboard"),
    path("admin_dashboard",views.dashboard,name="admin_dashboard"),

    # Orders

path(
    "orders/",
    views.order_list,
    name="dashboard_orders"
),

path(
    "orders/<int:id>/",
    views.order_detail,
    name="dashboard_order_detail"
),

path(
    "orders/<int:id>/approve/",
    views.approve_order,
    name="approve_order"
),

path(
    "orders/<int:id>/reject/",
    views.reject_order,
    name="reject_order"
),

path(
    "orders/<int:id>/cancel/",
    views.cancel_order,
    name="cancel_order"
),

path(
    "orders/<int:id>/deliver/",
    views.deliver_order,
    name="deliver_order"
),
]