from django.shortcuts import get_object_or_404, render
from .models import Product
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


# Create your views here.
def storePage(request, category_slug=None):
    products = None
    categories = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by("id")
        paginator = Paginator(products, 6)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context = {
        "products": paged_products,
        "product_count": product_count,
    }
    return render(request, "store/store.html", context)


def Productdetails(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug
        )
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=single_product
        ).exists()

    except Exception as e:
        raise e
    context = {
        "single_product": single_product,
        "in_cart": in_cart,
    }
    return render(request, "store/product_details.html", context)


def Search(request):
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        if keyword:
            product = Product.objects.order_by("-created_date").filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )
    context = {
        "products": product,
    }

    return render(request, "store/store.html", context)


def filter_price(request, min_val, max_val):
    products = Product.objects.filter(price__gte=min_val, price__lte=max_val).order_by(
        "-created_date"
    )
    context = {
        "products": products,
    }
    return render(request, "store/store.html", context)
