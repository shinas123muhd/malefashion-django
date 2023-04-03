from django.urls import path
from .import views


urlpatterns = [
    path('adminpanel/',views.AdminPanel,name = 'adminpanel'),
    path('adminproducts/',views.AdminProducts,name = 'adminproducts'),
    path('adminorders/',views.AdminOrders,name = 'adminorders'),
    path('adminusers/',views.AdminUsers,name = 'adminusers'),

]