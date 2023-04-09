import datetime
from django.shortcuts import render,redirect
from cart.models import CartItem

from .forms import OrderForm
from .models import Order

# Create your views here.

def PlaceOrder(request,total = 0,quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user = current_user)
    items_count = cart_items.count()
    if items_count <= 0:
        return redirect('store')
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid:
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.Phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%d'))
            dt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date * str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user=current_user, is_ordered=False, order_number = order_number)
            context ={
                'order': order,
                'cart_items' : cart_items,
                'total' : total,
                'tax' : tax,
                'grand_total' : grand_total,
            }
            return redirect ('checkout')
    else:
        return redirect ('checkout')

    
           


