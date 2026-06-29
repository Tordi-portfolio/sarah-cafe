from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from orders.models import Order
from django.contrib import messages

@login_required
def customer_dashboard(request):

    orders = Order.objects.filter(customer=request.user)

    context = {

        "total_orders": orders.count(),

        "member_since": request.user.date_joined,

    }

    return render(
        request,
        "dashboard/customer_dashboard.html",
        context
    )



from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required

from products.models import CoffeeProduct, Category
from orders.models import Order
from accounts.models import User


@staff_member_required
def dashboard(request):

    context = {

        "total_products": CoffeeProduct.objects.count(),

        "total_categories": Category.objects.count(),

        "total_orders": Order.objects.count(),

        "total_customers": User.objects.filter(
            role="customer"
        ).count(),

        "pending_orders": Order.objects.filter(
            status="Pending"
        ).count(),

    }

    return render(
        request,
        "dashboard/index.html",
        context
    )


@staff_member_required
def products(request):

    products = CoffeeProduct.objects.all()

    return render(
        request,
        "dashboard/products.html",
        {

            "products": products

        }

    )


@staff_member_required
def orders(request):

    orders = Order.objects.all().order_by("-created_at")

    return render(
        request,
        "dashboard/orders.html",
        {

            "orders": orders

        }

    )


@staff_member_required
def customers(request):

    customers = User.objects.filter(
        role="customer"
    )

    return render(
        request,
        "dashboard/customers.html",
        {

            "customers": customers

        }

    )


# This page is for admin only

@staff_member_required
def order_list(request):

    search = request.GET.get("search")

    orders = Order.objects.all().order_by("-created_at")

    if search:

        orders = orders.filter(

            full_name__icontains=search

        )

    return render(

        request,

        "dashboard/orders.html",

        {

            "orders": orders,

            "search": search

        }

    )


@staff_member_required
def order_detail(request, id):

    order = get_object_or_404(

        Order,

        id=id

    )

    return render(

        request,

        "dashboard/order_detail.html",

        {

            "order": order

        }

    )


@staff_member_required
def approve_order(request, id):

    order = get_object_or_404(

        Order,

        id=id

    )

    order.status = "Approved"

    order.save()

    messages.success(

        request,

        "Order Approved."

    )

    return redirect("dashboard_orders")


@staff_member_required
def reject_order(request, id):

    order = get_object_or_404(

        Order,

        id=id

    )

    order.status = "Rejected"

    order.save()

    messages.success(

        request,

        "Order Rejected."

    )

    return redirect("dashboard_orders")


@staff_member_required
def cancel_order(request, id):

    order = get_object_or_404(

        Order,

        id=id

    )

    order.status = "Cancelled"

    order.save()

    messages.success(

        request,

        "Order Cancelled."

    )

    return redirect("dashboard_orders")


@staff_member_required
def deliver_order(request, id):

    order = get_object_or_404(

        Order,

        id=id

    )

    order.status = "Delivered"

    order.save()

    messages.success(

        request,

        "Order Delivered."

    )

    return redirect("dashboard_orders")