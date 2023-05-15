from django.shortcuts import get_object_or_404, render
from .models import Product,Offer
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.utils import timezone
from decimal import Decimal



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
def Productoffer(request,product_id):
    product = Product.objects.get(id=product_id)
    offer = Offer.objects.filter(product=product).first()    
    discounted_price = None
    if offer:
        
        discounted_price = Decimal(product.price * (1 - offer.discount / 100)).quantize(Decimal('0.01'))
    
    context = {
        'product':product,
        'offer':offer,
        'discounted_price':discounted_price,
    }

    return render(request,'store/store.html',context)

def sortbyprice(request):
    
    sort_option = request.GET.get('sort_option')
    products = Product.objects.all()

    if sort_option == 'low_to_high':
        products = products.order_by('price')
    elif sort_option == 'high_to_low':
        products = products.order_by('-price')

    context = {
        'products':products,

    }
    return render(request,'store/store.html',context)
    

