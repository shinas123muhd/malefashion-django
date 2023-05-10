import datetime

from django.shortcuts import render, redirect
from cart.models import CartItem,Product
from django.http import HttpResponse, JsonResponse
from .forms import OrderForm
from .models import Order,Payment,OrderProduct
from accounts.models import Address
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from adminpart.models import Coupon
from django.contrib import messages
import json

# Create your views here.


def PlaceOrder(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    items_count = cart_items.count()
    if items_count <= 0:
        return redirect("store")
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        if cart_item.product.discount_price():
            total += cart_item.product.discount_price() * cart_item.quantity
        else:
            total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax
    disc_amount = 0

    coupon_code = request.session.get('coupon_code')
    if coupon_code:
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
            date = datetime.datetime.now().date()
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
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            
            data.Phone = form.cleaned_data["Phone"]
            
            data.address_line_1 = form.cleaned_data["address_line_1"]
            data.address_line_2 = form.cleaned_data["address_line_2"]
            data.state = form.cleaned_data["state"]
            data.city = form.cleaned_data["city"]
            data.pincode = form.cleaned_data["pincode"]
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()

            yr = int(datetime.date.today().strftime("%Y"))
            dt = int(datetime.date.today().strftime("%d"))
            mt = int(datetime.date.today().strftime("%m"))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number
            )
            payment_option = request.POST["payment_option"]
            print(grand_total)
            context = {
                "order": order,
                "cart_items": cart_items,
                "total": total,
                "tax": tax,
                "grand_total": grand_total,
            }
            if payment_option == "cod":
                return render(request, "order/cod.html", context)
            else:
                return render(request, "order/paypal.html", context)
        else:
            return HttpResponse("invalid data")
    else:
        return redirect("checkout")


def ConfirmOrder(request,order_number):
    if request.user.is_authenticated:
        
        
        order = Order.objects.get(user=request.user, is_ordered=False,order_number=order_number)
        

        order.is_ordered = True
        order.order_status = "Processing"
        order.save()
        
        cart_items = CartItem.objects.filter(user=request.user)
        
        for item in cart_items:
            order_product = OrderProduct()
            order_product.order_id = order.id
            order_product.user_id = request.user.id
            order_product.product_id = item.product_id
            order_product.quantity = item.quantity
            order_product.product_price = item.product.price
            order_product.ordered = True
            order_product.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            order_product = OrderProduct.objects.get(id=order_product.id)
            order_product.variations.set(product_variation)
            order_product.save()

            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

    CartItem.objects.filter(user=request.user).delete()

    mail_subject = 'Thank you for your order'
    message = render_to_string('order/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    
    
    return render(request, "order/cod_complete.html")


    


def CodComplete(request):
    return render(
        request,
        "order/cod_complete.html",
    )


def Paypalpay(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user,is_ordered = False,order_number = body['orderID'])
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status']
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    cart_items = CartItem.objects.filter(user =request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id = item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id = orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()


        product = Product.objects.get(id =item.product_id)
        product.stock -= item.quantity
        product.save()

    CartItem.objects.filter(user = request.user).delete()

    mail_subject = 'Thankyou for your order'
    message = render_to_string('order/order_recieved_email.html',{
        'user' :request.user,
        'order':order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()

    data = {
        'order_number':order.order_number,
        'transID' : payment.payment_id,
    }
    return JsonResponse(data)

    


def Codpay(request):
    return render(request, "order/cod.html")


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number = order_number,is_ordered = True)
        ordered_products = OrderProduct.objects.filter(order_id = order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity
        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order':order,
            'ordered_products':ordered_products,
            'order_number':order.order_number,
            'transID':payment.payment_id,
            'total':subtotal
        }
        return render(request,"order/order_complete.html",context)
    except (Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('Homepage')
