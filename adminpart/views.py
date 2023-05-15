import os
from django.shortcuts import render, redirect
from accounts.models import Account
from store.models import Product,Offer
from category.models import Category
from django.contrib.auth.decorators import login_required
from orders.models import Order,OrderProduct,Payment
from .models import Coupon
from datetime import datetime,timedelta
from django.db.models import Sum
from django.contrib import messages


# Create your views here.
def AdminPanel(request):
    if request.user.is_superadmin:
        Products = Product.objects.all()
        OrderedProducts = OrderProduct.objects.filter(ordered=True)
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        
        dates = [start_of_week + timedelta(days=i) for i in range(7)]

        sales = []
        for date in dates:
            orders = OrderProduct.objects.filter(
                ordered=True,
                created_at__year=date.year,
                created_at__month=date.month,
                created_at__day=date.day,
            )
            total_sales = sum(order.product_price * order.quantity for order in orders)
            sales.append(total_sales)
        
        

        context = {
            "Products": Products,
            "OrderedProducts":OrderedProducts,
            "dates":dates,
            "sales":sales
            
        }
        return render(request,'admin/adminpanel.html',context)
    
    return render(request, "admin/adminpanel.html")


def AdminUsers(request):
    if request.user.is_superadmin:
        Users = Account.objects.filter(is_admin=False).order_by("id")
        ordered_users = Order.objects.filter(is_ordered=True, status__in=["New", "Packed", "Shipped", "Cancelled", "Returned"]).exclude(status="Delivered").distinct("user").values_list("user", flat=True)
        user_count = Users.count()
        context = {
            "Users": Users,
            "user_count": user_count,
            "ordered_users":ordered_users
        }
        return render(request, "admin/adminusers.html", context)
    else:
        return redirect("login")


def AdminCategory(request):
    if request.user.is_superadmin:
        Categories = Category.objects.all().order_by("id")
        category_count = Categories.count()
        context = {
            "Categories": Categories,
            "category_count": category_count,
        }
        return render(request, "admin/admincategory.html", context)


def DltCategory(request, id):
    if request.user.is_superadmin:
        Categories = Category.objects.get(id=id)
        Categories.delete()
        return redirect("admincategory")
    else:
        return redirect("login")


def AddCategory(request):
    if request.user.is_superadmin:
        if request.method == "POST":
            category_name = request.POST["category_name"]
            description = request.POST["description"]
            cat_img = request.FILES["cat_img"]

            Category.objects.create(
                category_name=category_name,
                description=description,
                cat_img=cat_img,
            )
            Categories = Category.objects.all().order_by("id")
            category_count = Categories.count()
            context = {
                "Categories": Categories,
                "category_count": category_count,
            }
            return render(request, "admin/admincategory.html", context)
        else:
            return render(request, "admin/addcategory.html")
    else:
        return redirect("login")


def AdminProducts(request):
    if request.user.is_superadmin:
        Products = Product.objects.all().order_by("id")
        product_count = Products.count()

        context = {
            "Products": Products,
            "product_count": product_count,
        }
        return render(request, "admin/adminproducts.html", context)
    else:
        return redirect("login")


def EditCategory(request, id):
    if request.user.is_superadmin:
        if request.method == "POST":
            Category.objects.filter(id=id).update(
                category_name=request.POST["category_name"],
                description=request.POST["description"],
            )
            return redirect("admincategory")
        else:
            context = {
                "category": Category.objects.get(id=id),
            }
            return render(request, "admin/editcategory.html", context)
    else:
        return redirect("login")


@login_required(login_url="login")
def AddProduct(request):
    if request.user.is_superadmin:
        Categories = Category.objects.all()
        if request.method == "POST":
            product_name = request.POST["product_name"]
            description = request.POST["description"]
            price = request.POST["price"]
            image = request.FILES["image"]
            stock = request.POST["stock"]
            category_id = request.POST["category"]
            category = Category.objects.get(id=category_id)

            new_product = Product.objects.create(
                product_name=product_name,
                description=description,
                price=price,
                image=image,
                stock=stock,
                category=category,
            )
            Products = Product.objects.all().order_by("id")
            product_count = Products.count()

            context = {
                "Products": Products,
                "product_count": product_count,
            }
            return render(request, "admin/adminproducts.html", context)
        else:
            context = {
                "Categories": Categories,
            }
            return render(request, "admin/addproduct.html", context)
    else:
        return redirect("login")


def DltProduct(request, id):
    if request.user.is_superadmin:
        prod = Product.objects.get(id=id)
        prod.delete()
        return redirect("adminproducts")
    else:
        return redirect("login")


def EditProduct(request, id):
    if request.user.is_superadmin:
        prod = Product.objects.get(id=id)
        if request.method == "POST":
            Product.objects.filter(id=id).update(
                product_name=request.POST["product_name"],
                description=request.POST["description"],
                price=request.POST["price"],
                stock=request.POST["stock"],
            )
            return redirect("adminproducts")

        else:
            prod = Product.objects.get(id=id)
            context = {"product": Product.objects.get(id=id)}
            return render(request, "admin/editproduct.html", context)
    else:
        return redirect("login")


def AdminOrders(request):
    if request.user.is_authenticated:
        Orders = Order.objects.filter(is_ordered = True).order_by("-id")
        
        order_count = Orders.count()

        for order in Orders:
            payment_method = ""
            if order.payment:
                payment_method = order.payment.payment_method
            else:
                payment_method = "COD"
            
            order.payment_method = payment_method
        
        
        context = {
            "Orders": Orders,
            "order_count": order_count,
            
            
        }
        return render(request, "admin/adminorders.html", context)
    else:
        return redirect("login")


def blockuser(request, id, action):
    if request.user.is_superadmin:
        user = Account.objects.get(id=id)
        if action == "block":
            user.is_active = False
            user.save()
        elif action == "unblock":
            user.is_active = True
            user.save()
        return redirect("adminusers")
    else:
        return redirect("login")


def OrderStatus(request, id, action):
    if request.user.is_authenticated:
        order = Order.objects.get(id=id)
        if action == "Packed":
            order.status = "Packed"
            order.save()
        elif action == "Shipped":
            order.status = "Shipped"
            order.save()
        elif action == "Delivered":
            order.status = "Delivered"
            order.save()
        return redirect("adminorders")
    else:
        return redirect("login")


def cancelOrder(request, id):
    if request.user.is_authenticated:
        order = Order.objects.get(id=id)        
        order_products = OrderProduct.objects.filter(order=order)       
        for order_product in order_products:
            product = order_product.product
            
            product.stock += order_product.quantity
            
            
            product.save()        
        order.delete()
        return redirect("adminorders")
    else:
        return redirect("login")


def viewOrderItems(request, id):
    if request.user.is_authenticated:
        
        Orders = Order.objects.filter(id=id).order_by("-id")
        ordered_products = OrderProduct.objects.filter(order_id = id)
        order_count = Orders.count()
        context = {
            "Orders": Orders,
            "order_count": order_count,
            "ordered_products":ordered_products,
        }
        return render(request, "admin/vieworders.html", context)
    else:
        return redirect('login')
def createcoupon(request):
    if request.user.is_superadmin:
        if request.method == "POST":
            coupon_code = request.POST['coupon_code']
            min_amount = request.POST['min_amount']
            active_date_str = request.POST['active_date']
            expire_date_str = request.POST['expire_date']
            discount_amount = request.POST['discount_amount']

            active_date = datetime.strptime(active_date_str, "%m/%d/%Y").date()
            expire_date = datetime.strptime(expire_date_str, "%m/%d/%Y").date()

            Coupon.objects.create(
                coupon_code = coupon_code,
                min_amount = min_amount,
                active_date = active_date,
                expire_date = expire_date,
                discount_amount = discount_amount

            )
            coupons = Coupon.objects.all().order_by('-id')
            coupon_count = coupons.count()
            context = {
                'coupons':coupons,
                'coupon_count':coupon_count
            }
            return render(request,'admin/coupons.html',context)
        else:
            return render(request,'admin/addcoupon.html')
    else:
        return redirect('login')


def coupon(request):
    if request.user.is_authenticated:
        coupons = Coupon.objects.all().order_by('-id')
        coupon_count = coupons.count()
        context = {
            'coupons':coupons,
            'coupon_count':coupon_count
        }
        return render(request,'admin/coupons.html',context)
    else:
        return redirect('login')
    
def deletecoupon(request,id):
    if request.user.is_superadmin:
        Acoupon = Coupon.objects.filter(id=id)
        Acoupon.delete()
        return redirect('coupon')
    else:
        return redirect('login')
    

def filterOrders(request,start_date_str,end_date_str):
    if request.method =="POST":
        start_date_str = request.POST['start_date']
        end_date_str = request.POST['end_date']
        start_date = datetime.strptime(start_date_str, "%m/%d/%Y").date()
        end_date = datetime.strptime(end_date_str, "%m/%d/%Y").date()
        if start_date > end_date:
            messages.error(request,'Starting date should be less')
            return redirect('adminreport')
        filteredorders = Order.objects.filter(created_at__gte=start_date, created_at__lte=end_date,is_ordered = True).order_by('-created_at')
        for order in filteredorders:
            payment_method = ""
            if order.payment:
                payment_method = order.payment.payment_method
            else:
                payment_method = "COD"
            
            order.payment_method = payment_method
        context ={
            'filteredorders':filteredorders,
        }
        
        
        return render(request,'admin/adminreport.html',context)
    
def adminreport(request):
    if request.user.is_authenticated:
        Orders = Order.objects.filter(is_ordered = True).order_by("-id")
        
        order_count = Orders.count()

        for order in Orders:
            payment_method = ""
            if order.payment:
                payment_method = order.payment.payment_method
            else:
                payment_method = "COD"
            
            order.payment_method = payment_method
        
        
        context = {
            "Orders": Orders,
            "order_count": order_count,
            
            
        }
        return render(request, "admin/adminreport.html", context)
    else:
        return redirect("login")
    
def addoffer(request):
    if request.user.is_superadmin:
        products = Product.objects.all()
        if request.method =="POST":
            discount = request.POST["discount"]                      
            product_id = request.POST["product"]
            product = Product.objects.get(id=product_id)
            new_offer = Offer.objects.create(
                discount = discount,
                product=product
            )
            offers = Offer.objects.all().order_by('-id')
            context ={
                'offers':offers,

            }
            return render(request,'admin/adminoffer.html',context)
        else:
            context = {
                'products':products,
            }
            return render(request,'admin/addoffer.html',context)
    return redirect('login')

def adminoffers(request):
    if request.user.is_superadmin:
        offers = Offer.objects.all().order_by('-id')
        context ={
            'offers':offers,
        }
        return render(request,'admin/adminoffer.html',context)
    else:
        return redirect('login')
    
def deleteoffers(request,offer_id):
    if request.user.is_superadmin:
        offer = Offer.objects.get(id=offer_id)
        offer.delete()
        return redirect('adminoffers')
    else:
        return redirect('login')

    


    


    
    



