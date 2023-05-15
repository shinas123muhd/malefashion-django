import json
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegistrationForm, UserForm, UserProfileForm,OTPRegistrationForm,Verifyform
from .models import Account, UserProfile, Address
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse,JsonResponse
from cart.models import Cart, CartItem
from cart.views import _cart_id
from category.models import Category
import requests
from orders.models import Order,OrderProduct
from . import verify
from adminpart.models import Coupon
from datetime import datetime


# Create your views here.
def RegisterPage(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            user = Account.objects.create_user(
                username=username, email=email, password=password
            )
            user.phone_number = phone_number
            user.save()

            current_site = get_current_site(request)
            mail_subject = "Click the link to activate your account"
            message = render_to_string(
                "accounts/verification_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request,"Check your email for the verification link")
            return redirect("/accounts/login/?command=verification&email=" + email)

    else:
        form = RegistrationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/register.html", context)

def registerotp(request):
    if request.method == "POST":
        form = OTPRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = Account.objects.create_user(
                username=username, phone_number=phone_number,password=password,email=email
            )

            
            user.save()
            verify.send(form.cleaned_data.get('phone_number'))
            request.session['email']=user.email
            return redirect('otpverify')
        
            
            
    else:
        form = OTPRegistrationForm()
    context ={
        "form":form,
    }

    return render(request,'accounts/registerotp.html',context)

def otpverify(request):
    user_email = request.session.get('email')
    user = get_object_or_404(Account,email = user_email)
    print(user_email)
    
    if request.method =="POST":
        form = Verifyform(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            print(code)
            if verify.check(user.phone_number, code):
                
                user.is_active = True
                user.save()
                return redirect('login')
                
    else:
        form = Verifyform()
    context = {
        'form':form,
    }
    return render(request, 'accounts/verifyotp.html',context)


def LoginPage(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            if user.is_admin:
                auth.login(request, user)
                return render(request, "admin/adminpanel.html")
            else:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart=cart).order_by("id")

                        production_variation = []
                        for item in cart_item:
                            variation = item.variations.all()
                            production_variation.append(list(variation))

                        cart_item = CartItem.objects.filter(user=user).order_by("id")
                        ex_var_list = []
                        id = []
                        for item in cart_item:
                            existing_variation = item.variations.all()
                            ex_var_list.append(list(existing_variation))
                            id.append(item.id)

                        for pr in production_variation:
                            if pr in ex_var_list:
                                index = ex_var_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity += 1
                                item.user = user
                                item.save()
                            else:
                                cart_item = CartItem.objects.filter(cart=cart).order_by(
                                    "id"
                                )
                                for item in cart_item:
                                    item.user = user
                                    item.save()

                except:
                    pass
                auth.login(request, user)
                url = request.META.get("HTTP_REFERER")
                try:
                    query = requests.utils.urlparse(url).query
                    params = dict(x.split("=") for x in query.split("&"))
                    if "next" in params:
                        nextPage = params["next"]
                        return redirect(nextPage)
                except:
                    return redirect("Homepage")
        else:
            messages.error(request, "User is not Active")
            return redirect("login")
    return render(request, "accounts/login.html")


@login_required(login_url="login")
def LogoutPage(request):
    auth.logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("login")


def activatePage(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Successfully activated your account")
        return redirect("login")
    else:
        messages.error(request, "Invalid activation link")
        return redirect("register")


@login_required(login_url="login")
def DashboardPage(request):
    user = request.user
    order = Order.objects.filter(user=user,is_ordered=True)
    order_count = order.count()
    profile = UserProfile.objects.get(user=user)
    addresses = Address.objects.filter(profile=profile)
    context = {
        "user":user,
        "order_count": order_count,
        'profile':profile,
        'addresses':addresses,
    }
    return render(request, "accounts/dashboard.html", context)


@login_required(login_url="login")
def forgotpasswordPage(request):
    if request.method == "POST":
        email = request.POST["email"]
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)
            current_site = get_current_site(request)
            mail_subject = "Reset your password"
            message = render_to_string(
                "accounts/reset_passwordvalidate.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(
                request, "Password reset email has been sent to your email account"
            )
            return redirect("login")
        else:
            messages.error(request, "Account doesn't exist")
            return redirect("forgotpassword")

    return render(request, "accounts/forgotpassword.html")


@login_required(login_url="login")
def ResetpasswordValidate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Please reset your password")
        return redirect("resetpassword")
    else:
        messages.error(request, "Invalid activation link")
        return redirect("login")


@login_required(login_url="login")
def resetpasswordPage(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            uid = request.session.get("uid")
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful")
            return redirect("login")
        else:
            messages.error(request, "Password does'nt match")
            return redirect("resetpassword")
    else:
        return render(request, "accounts/resetpassword.html")


@login_required(login_url="login")
def editprofilePage(request):
    user = request.user
    try:
        userprofile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        userprofile = None
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, "Your Profile has been Updated")
            return redirect("editprofile")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(request, "accounts/editprofile.html", context)


@login_required(login_url="login")
def ChangepasswordPage(request):
    if request.method == "POST":
        currentpassword = request.POST["currentpassword"]
        newpassword = request.POST["newpassword"]
        confirmpassword = request.POST["confirmpassword"]

        user = Account.objects.get(username=request.user.username)
        if newpassword == confirmpassword:
            success = user.check_password(currentpassword)
            if success:
                user.set_password(confirmpassword)
                user.save()
                messages.success(request, "successfully changed password")
                return redirect("changepassword")
            else:
                messages.error(request, "You have entered a wrong current password")
                return redirect("changepassword")
        else:
            messages.error(request, "Both passwords need to be same")
            return redirect("changepassword")

    return render(request, "accounts/changepassword.html")


@login_required(login_url="login")
def add_address(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            profile = UserProfile.objects.get(user=user)
            Address.objects.create(
                profile=profile,
                address_line_1=request.POST["address_line_1"],
                address_line_2=request.POST["address_line_2"],
                city=request.POST["city"],
                state=request.POST["state"],
                pincode=request.POST["pincode"],
                phone=request.POST["phone"],
            )
            messages.success(request, "Successfully added address")
            return redirect("dashboard")

        else:
            return render(request, "accounts/addaddress.html")
    else:
        return redirect("login")


@login_required(login_url="login")
def order_details(request):
    user = request.user
    Orders = Order.objects.filter(user=user,is_ordered = True)
    order_count = Orders.count()
    context = {
        "Orders": Orders,
        "order_count": order_count,
    }

    return render(request, "accounts/order_details.html", context)


@login_required(login_url="login")
def cancelorderUser(request, id):
    
    if request.user.is_authenticated:
        order = Order.objects.get(id=id)        
        order_products = OrderProduct.objects.filter(order=order)       
        for order_product in order_products:
            product = order_product.product
            
            product.stock += order_product.quantity
            
            
            product.save()        
        order.delete()
        return redirect("orderdetails")
    


def selectAddress(request):
    if request.method == "POST":
        body = json.loads(request.body)    
        qty = Address.objects.get(id=body["id"])
        address_line_1 = qty.address_line_1
        address_line_2 = qty.address_line_2
        city = qty.city
        state = qty.state
        pincode = qty.pincode
        phone = qty.phone
        data = {
            "address_line_1": address_line_1,
            "address_line_2": address_line_2,
            "city" : city,
            "state" : state,
            "pincode" : pincode,
            "phone" : phone,
            
        }
        return JsonResponse(data)
    



def contactus(request):
    return render(request,'contact.html')
def printinvoice(request,id):
    if request.user.is_authenticated:
        order = Order.objects.get(id = id)
        ordered_products = OrderProduct.objects.filter(order_id = id)
        tax = 0
        grand_total = 0
        discount_a=0
        subtotal = 0
        for i in ordered_products:
            if i.product.discount_price():
                subtotal += round(i.product.discount_price() * i.quantity,2)
            else:            
                subtotal += i.product_price * i.quantity
        disc_amount = 0
        tax = round((2 * subtotal) / 100,2)
        coupon_code = request.session.get('coupon_code')
        if coupon_code:
             
            try:
                coupon = Coupon.objects.get(coupon_code=coupon_code)
                date = datetime.now().date()
                s_date = coupon.active_date
                l_date = coupon.expire_date
                mini_amount = coupon.min_amount
                disc_amount = coupon.discount_amount

                if (int(mini_amount) < int(subtotal) and s_date <= date <= l_date):
                    coupon_discount = int(disc_amount)
                    grand_total = subtotal - coupon_discount + tax
                else:
                    request.session['coupon_code'] = None
                    messages.error(request, 'Invalid coupon code')
                    print("hello")
            except Coupon.DoesNotExist:
                request.session['coupon_code'] = None
                messages.error(request, 'Invalid coupon code')
                disc_amount = None
                print("hii")
        grand_total = subtotal + tax - int(disc_amount)
        discount_a = order.order_total - (subtotal+tax)
        print(discount_a)
        print(disc_amount)
        context = {
            'order':order,
            'discount_a':discount_a,
            'ordered_products':ordered_products,
            'grand_total':grand_total,            
            'total':subtotal,
        }
        return render(request,'accounts/invoice.html',context)
    
def returnorder(request,id):
    if request.user.is_authenticated:
        order = Order.objects.get(id=id)        
        order_products = OrderProduct.objects.filter(order=order)       
        for order_product in order_products:
            product = order_product.product
            
            product.stock += order_product.quantity
            
            
            product.save()        
        order.delete()
    return redirect('orderdetails')
def aboutus(request):
    categories = Category.objects.all()
    category_count = categories.count()
    users = Account.objects.filter(is_admin = False)
    users_count = users.count()

    context ={
        'category_count':category_count,
        'users_count':users_count
    }
    return render(request,'aboutus.html',context)
