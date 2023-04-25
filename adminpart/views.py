import os
from django.shortcuts import render, redirect
from accounts.models import Account
from store.models import Product
from category.models import Category
from django.contrib.auth.decorators import login_required
from orders.models import Order


# Create your views here.
def AdminPanel(request):
    return render(request, "admin/adminpanel.html")


def AdminUsers(request):
    if request.user.is_superadmin:
        Users = Account.objects.filter(is_admin=False).order_by("id")
        user_count = Users.count()
        context = {
            "Users": Users,
            "user_count": user_count,
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
            return render(request, "admin/addproduct.html", context)
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
        order = Order.objects.filter(id=id)
        order.delete()
        return redirect("adminorders")
    else:
        return redirect("login")


def viewOrderItems(request, id):
    if request.user.is_authenticated:
        Orders = Order.objects.filter(id=id).order_by("-id")
        order_number = Orders.count()
        context = {
            "Orders": Orders,
            "order_number": order_number,
        }
        return render(request, "admin/vieworders.html", context)
