from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from .forms import RegisterForm


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(request, "Account created successfully.")

            return redirect("home")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]

        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            messages.success(request, "Welcome back!")

            return redirect("home")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, "accounts/login.html")


def logout_view(request):

    logout(request)

    messages.success(request, "Logged out successfully.")

    return redirect("home")



from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from orders.models import Order


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        customer=request.user
    ).order_by("-created_at")

    context = {
        "orders": orders
    }

    return render(
        request,
        "orders/my_orders.html",
        context
    )