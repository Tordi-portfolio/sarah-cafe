from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from .models import CoffeeProduct, Category


def shop(request):
    # Get all available products
    products = CoffeeProduct.objects.filter(available=True).select_related("category")

    categories = Category.objects.all()

    # Search
    search_query = request.GET.get("search", "").strip()

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(origin__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Category Filter
    category_slug = request.GET.get("category")

    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Sorting
    sort = request.GET.get("sort")

    if sort == "price_low":
        products = products.order_by("price")

    elif sort == "price_high":
        products = products.order_by("-price")

    elif sort == "name":
        products = products.order_by("name")

    elif sort == "newest":
        products = products.order_by("-created_at")

    # Pagination
    paginator = Paginator(products, 9)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "categories": categories,
        "search_query": search_query,
        "selected_category": category_slug,
        "selected_sort": sort,
    }

    return render(request, "products/shop.html", context)


def product_detail(request, slug):
    product = get_object_or_404(
        CoffeeProduct,
        slug=slug,
        available=True,
    )

    related_products = CoffeeProduct.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]

    context = {
        "product": product,
        "related_products": related_products,
    }

    return render(
        request,
        "products/product_detail.html",
        context,
    )


# THIS IS THE ADMIN PAGE


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from products.models import CoffeeProduct
from products.forms import ProductForm


@staff_member_required
def product_list(request):

    products = CoffeeProduct.objects.all().order_by("-created_at")

    return render(
        request,
        "dashboard/products.html",
        {
            "products": products
        }
    )


@staff_member_required
def add_product(request):

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Product added successfully."
            )

            return redirect("dashboard_products")

    else:

        form = ProductForm()

    return render(
        request,
        "dashboard/product_form.html",
        {
            "form": form,
            "title": "Add Product"
        }
    )


@staff_member_required
def edit_product(request, id):

    product = get_object_or_404(
        CoffeeProduct,
        id=id
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Product updated successfully."
            )

            return redirect("dashboard_products")

    else:

        form = ProductForm(instance=product)

    return render(
        request,
        "dashboard/product_form.html",
        {
            "form": form,
            "title": "Edit Product"
        }
    )


@staff_member_required
def delete_product(request, id):

    product = get_object_or_404(
        CoffeeProduct,
        id=id
    )

    product.delete()

    messages.success(
        request,
        "Product deleted successfully."
    )

    return redirect("dashboard_products")


def category_list(request):
    return render(request, 'category_list.html')