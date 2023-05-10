from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from store.models import Product, Variation
from .models import Cart, CartItem, Wishlist
from adminpart.models import Coupon
from django.contrib.auth.decorators import login_required
import json
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import UserProfile, Address
from django.core.serializers import serialize
from django.contrib import messages


# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
        

    if current_user.is_authenticated:
        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value,
                    )
                    product_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(
            product=product, user=current_user
        ).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)

            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(
                    product=product, quantity=1, user=current_user
                )
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )

            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        return redirect("cart")

    else:
        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value,
                    )
                    product_variation.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(
            product=product, cart=cart
        ).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)

            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )

            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        return redirect("cart")


def remove_item_cart(request, id):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(id=id)
    # else:

    #     cart = Cart.objects.get(cart_id = _cart_id(request))
    #     cart_item = CartItem.objects.get(id = id)
    cart_item.delete()
    return redirect("cart")


def wishlist_Page(request):
    user_name = request.user
    wlist_items = Wishlist.objects.filter(user=user_name)
    w_list_count = wlist_items.count()
    context = {
        "wlist_items": wlist_items,
        "w_list_count": w_list_count,
    }
    return render(request, "wishlist.html", context)


def addwish(request, product_id):
    user_name = request.user
    products = Product.objects.get(id=product_id)

    if Wishlist.objects.filter(product=products, user=user_name).exists():
        return redirect("wishlist")
    else:
        Wishlist.objects.create(product=products, user=user_name)
        return redirect("wishlist")


def removewish(request, product_id):
    wish_item = Wishlist.objects.get(id=product_id)
    wish_item.delete()
    return redirect("wishlist")


def CartPage(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True
            ).order_by("id")
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by(
                "id"
            )
        for cart_item in cart_items:
            if cart_item.product.discount_price():
                total += cart_item.product.discount_price() * cart_item.quantity
            else:
                total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = round(tax + total,2)

    except ObjectDoesNotExist:
        pass

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total,
    }

    return render(request, "store/cart.html", context)


@login_required(login_url="login")
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            if cart_item.product.discount_price():
                total += cart_item.product.discount_price() * cart_item.quantity
            else:
                total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = tax + total
        disc_amount = 0

        coupon_code = request.session.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon.objects.get(coupon_code=coupon_code)
                date = datetime.now().date()
                s_date = coupon.active_date
                l_date = coupon.expire_date
                mini_amount = coupon.min_amount
                disc_amount = coupon.discount_amount

                if (int(mini_amount) < int(total) and s_date <= date <= l_date):
                    coupon_discount = int(disc_amount)
                    grand_total = total - coupon_discount + tax
                else:
                    request.session['coupon_code'] = None
                    messages.error(request, 'Invalid coupon code')
            except Coupon.DoesNotExist:
                request.session['coupon_code'] = None
                messages.error(request, 'Invalid coupon code')
                disc_amount = None
                

                
        grand_total = total + tax - int(disc_amount)

    except ObjectDoesNotExist:
        pass

    profile = UserProfile.objects.get(user=request.user)
    Addresses = Address.objects.filter(profile=profile)

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": '{:.2f}'.format(grand_total),
        "Addresses": Addresses,
    }

    return render(request, "store/checkout.html", context)


def remove_cart(request):
    body = json.loads(request.body)
    qty = CartItem.objects.get(id=body["id"])
    qty.quantity -= 1
    qty.save()
    str = "true"
    iquantity = qty.quantity
    total_subtotal = 0
    quantity = 0
    tax = 0
    total = 0
    cart_items = CartItem.objects.filter(user=request.user, is_active=True).order_by(
        "id"
    )
    for cart_item in cart_items:
        if cart_item.product.discount_price():
            sub_total = cart_item.quantity * cart_item.product.discount_price()
        else:
            sub_total = cart_item.quantity * cart_item.product.price
        
        total += sub_total
        quantity += cart_item.quantity
    print(sub_total)
    tax = (2 * total) / 100
    grand_total = tax + total
    data = {
        'total': total,
        'quantity': iquantity,
        'data': str,
        'grand_total':grand_total,
        'tax':tax,
        'sub_total':sub_total,
    }
    print(data)
    return JsonResponse(data)



def plus_cart(request):
    body = json.loads(request.body)
    qty = CartItem.objects.get(id=body["id"])
    prod = qty.product

    if prod.stock > qty.quantity:
        qty.quantity += 1
        qty.save()
        str = "true"
        iquantity = qty.quantity

        quantity = 0
        tax = 0
        total = 0
        cart_items = CartItem.objects.filter(user=request.user, is_active=True).order_by(
            "id"
        )
        for cart_item in cart_items:
            if cart_item.product.discount_price():
                sub_total = cart_item.quantity * cart_item.product.discount_price()
            else:
                sub_total = cart_item.quantity * cart_item.product.price
            total += sub_total
            quantity += cart_item.quantity
        print(sub_total)
        tax = (2 * total) / 100
        grand_total = tax + total
        data = {
            'total': total,
            'quantity': iquantity,
            'data': str,
            'grand_total':grand_total,
            'tax':tax,
            'sub_total':sub_total,
        }
        print(data)
        return JsonResponse(data)
    else:
        data = {
            'stock' : False
        }
        return JsonResponse(data)
    
def applycoupon(request):
    body = json.loads(request.body)
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    coupon_code = body['coupon']
    
    total =0
    for i in range(len(cart_items)):
        x = cart_items[i].product.price*cart_items[i].quantity
        total = total+x

    tax = (2 * total) / 100
    total = total+tax
    try:
        coupon = Coupon.objects.get(coupon_code=coupon_code)
               
    except Coupon.DoesNotExist:
        data ={
            'g_total':total,
            'coupon_id':"does not exist"
        }
        return JsonResponse(data)
    else:
        date = datetime.now().date()
        s_date = coupon.active_date
        l_date = coupon.expire_date
        mini_amount = coupon.min_amount
        disc_amount = coupon.discount_amount

        if (int(mini_amount) < int(total) and s_date <= date <= l_date):
            g_total = total-int(disc_amount)
            
            request.session['coupon_code'] = coupon_code
            data ={
                'g_total': '{:.2f}'.format(g_total),
                'coupon_id':"Applied Coupon : "+coupon_code
            }
            return JsonResponse(data)
        else:
            data = {
                'g_total':total,
                'coupon_id':"Minimal Cart Value"
            }

            return JsonResponse(data)
