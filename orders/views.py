from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from decimal import Decimal
from .forms import CheckoutForm
from .models import Order, OrderItem

from .models import Cart, CartItem
from products.models import CoffeeProduct


@login_required
def cart(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        "orders/cart.html",
        {
            "cart": cart
        }
    )


@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(
        CoffeeProduct,
        id=product_id,
        available=True
    )

    quantity = int(request.POST.get("quantity", 1))

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if created:
        item.quantity = quantity
    else:
        item.quantity += quantity

    # Prevent adding more than available stock
    if item.quantity > product.stock:
        item.quantity = product.stock

    item.save()

    return redirect("cart")


@login_required
def remove_from_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.delete()

    return redirect("cart")


from django.http import JsonResponse

@login_required
def checkout(request):

    cart, created = Cart.objects.get_or_create(user=request.user)

    if not cart.items.exists():
        return redirect("cart")

    if request.method == "POST":

        form = CheckoutForm(request.POST)

        if form.is_valid():

            order = form.save(commit=False)
            order.customer   = request.user
            order.total_price = cart.total
            order.save()

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                    subtotal=item.subtotal,
                )

            cart.items.all().delete()

            # AJAX request from the checkout template — return JSON so
            # the page can show Step 2 (bank details) without redirecting.
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"ok": True, "order_id": order.id})

            # Fallback for any plain (non-AJAX) POST.
            return redirect("order_success")

        else:
            # Return validation errors so the template can show them inline.
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"ok": False, "errors": form.errors})

    else:
        form = CheckoutForm()

    return render(
        request,
        "orders/checkout.html",
        {"form": form, "cart": cart},
    )


@login_required
def order_success(request):
    return render(request, "orders/order_success.html")