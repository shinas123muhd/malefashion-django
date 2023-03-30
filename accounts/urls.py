from django.urls import path
from .import views


urlpatterns = [
    
    path('register/',views.RegisterPage,name = 'register'),
    path('login/',views.LoginPage,name = 'login'),
    path('logout/',views.LogoutPage,name = 'logout'),
    path('dashboard/',views.DashboardPage,name = 'dashboard'),
    path('forgotpassword/',views.forgotpasswordPage,name = 'forgotpassword'),
    path('activate/<uidb64>/<token>/',views.activatePage,name = 'activate'),
    path('resetpasswordvalidate/<uidb64>/<token>/',views.ResetpasswordValidate,name = 'resetpasswordvalidate'),
    path('resetpassword/',views.resetpasswordPage,name = 'resetpassword'),
    path('editprofile/',views.editprofilePage,name = 'editprofile'),
    path('changepassword/',views.ChangepasswordPage,name = 'changepassword'),
    

]