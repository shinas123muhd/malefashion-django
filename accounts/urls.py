from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.RegisterPage, name="register"),
    path("login/", views.LoginPage, name="login"),
    path("logout/", views.LogoutPage, name="logout"),
    path("dashboard/", views.DashboardPage, name="dashboard"),
    path("forgotpassword/", views.forgotpasswordPage, name="forgotpassword"),
    path("activate/<uidb64>/<token>/", views.activatePage, name="activate"),
    path(
        "resetpasswordvalidate/<uidb64>/<token>/",
        views.ResetpasswordValidate,
        name="resetpasswordvalidate",
    ),
    path("resetpassword/", views.resetpasswordPage, name="resetpassword"),
    path("editprofile/", views.editprofilePage, name="editprofile"),
    path("changepassword/", views.ChangepasswordPage, name="changepassword"),
    path("addaddress/", views.add_address, name="addaddress"),
    path("orderdetails/", views.order_details, name="orderdetails"),
    path("cancelorderuser/<int:id>/", views.cancelorderUser, name="cancelorderuser"),
    path("selectaddress/", views.selectAddress, name="selectaddress"),
    path("contactus/", views.contactus, name="contactus"),
    path("printinvoice/<int:id>/", views.printinvoice, name="printinvoice"),
    path("registerotp/", views.registerotp, name="registerotp"),
    path("otpverify/", views.otpverify, name="otpverify"),
    path("returnorder/<int:id>/", views.returnorder, name="returnorder"),
    path("aboutus/", views.aboutus, name="aboutus"),
]
