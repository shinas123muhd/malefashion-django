
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from store.models import Product,Variation
from .models import Cart,CartItem
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist
from accounts.models import UserProfile,Address


# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
    return cart

def add_cart(request,product_id):
    product = Product.objects.get(id = product_id)
    product_variation = []
    if request.method =="POST":
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(product =product,variation_category__iexact = key,variation_value__iexact = value)
                product_variation.append(variation)
            except:
                pass
    
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product = product,cart = cart)
        
        if len(product_variation) > 0:
            cart_item.variation.clear()
            for item in product_variation:
                cart_item.variation.add(item)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity =1,
            cart = cart,
        )
        
        if len(product_variation) > 0:
            cart_item.variation.clear()
            for item in product_variation:
                cart_item.variation.add(item)
    cart_item.save()
    
    return redirect('cart')

def remove_cart(request,product_id):
    cart= Cart.objects.get(cart_id= _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product = product,cart = cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_item_cart(request,product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product,id = product_id)
    cart_item = CartItem.objects.get(product= product,cart=cart)
    cart_item.delete()
    return redirect('cart')



def CartPage(request,total=0,quantity=0,cart_items=None):
    tax = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart,is_active = True).order_by('id')
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = tax+total

    except ObjectDoesNotExist:
        pass

    context ={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax' : tax,
        'grand_total':grand_total

    }
    
    return render(request,"store/cart.html",context)
@login_required(login_url = 'login')
def checkout(request,total=0,quantity=0,cart_items=None):
    tax = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart,is_active = True).order_by('id')
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = tax+total

    except ObjectDoesNotExist:
        pass

    context ={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax' : tax,
        'grand_total':grand_total

    }

    return render(request,'store/checkout.html',context)