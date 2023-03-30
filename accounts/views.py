
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegistrationForm,UserForm,UserProfileForm
from .models import Account,UserProfile
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse


# Create your views here.
def RegisterPage(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = Account.objects.create_user(username=username,email=email,password=password)
            user.phone_number = phone_number
            user.save()

            current_site = get_current_site(request)
            mail_subject= "Click the link to activate your account"
            message = render_to_string('accounts/verification_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),            
            })
            to_email=email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            #messages.success(request,"Check your email for the verification link")
            return redirect("/accounts/login/?command=verification&email="+email)
        
    else:                    
        form = RegistrationForm()
    context = {
        'form':form,
    }
    return render(request,'accounts/register.html',context)

def LoginPage(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('Homepage')
        else:
            messages.error(request,'Invalid login credentials')
            return redirect('login')
    return render(request,'accounts/login.html')
@login_required(login_url = 'login' )
def LogoutPage(request):
    auth.logout(request)
    messages.success(request,"Successfully logged out")
    return redirect('login')

def activatePage(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk = uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"Successfully activated your account")
        return redirect('login')
    else:
        messages.error(request,"Invalid activation link")
        return redirect('register')

@login_required(login_url='login')
def DashboardPage(request):
    return render(request,'accounts/dashboard.html')
@login_required(login_url='login')
def forgotpasswordPage(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)
            current_site = get_current_site(request)
            mail_subject= "Reset your password"
            message = render_to_string('accounts/reset_passwordvalidate.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),            
            })
            to_email=email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request,"Password reset email has been sent to your email account")
            return redirect('login')        
        else:
            messages.error(request,"Account doesn't exist")
            return redirect('forgotpassword')


    return render(request,'accounts/forgotpassword.html')
def ResetpasswordValidate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk = uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,"Please reset your password")
        return redirect('resetpassword')
    else:
        messages.error(request,"Invalid activation link")
        return redirect('login')
@login_required(login_url='login')    
def resetpasswordPage(request):
    if request.method =='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password==confirm_password:
            uid = request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,"Password reset successful")
            return redirect('login')
        else:
            messages.error(request,"Password does'nt match")
            return redirect('resetpassword')
    else:
        return render(request,'accounts/resetpassword.html')
@login_required(login_url='login')    
def editprofilePage(request):
    user = request.user
    try:
        userprofile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        userprofile = None
    if request.method =="POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"Your Profile has been Updated")
            return redirect('editprofile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            
        }


    return render(request,"accounts/editprofile.html",context)
@login_required(login_url='login')
def ChangepasswordPage(request):
    if request.method =="POST":
        currentpassword = request.POST['currentpassword']
        newpassword = request.POST['newpassword']
        confirmpassword = request.POST['confirmpassword']

        user = Account.objects.get(username = request.user.username)
        if newpassword==confirmpassword:
            success = user.check_password(currentpassword)
            if success:
                user.set_password(confirmpassword)
                user.save()
                messages.success(request,"successfully changed password")
                return redirect('changepassword')
            else:
                messages.error(request,"You have entered a wrong current password")
                return redirect('changepassword')
        else:
            messages.error(request,"Both passwords need to be same")
            return redirect('changepassword')
            

    return render(request,'accounts/changepassword.html')

    