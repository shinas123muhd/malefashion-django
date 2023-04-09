from django.urls import path
from .import views


urlpatterns = [
    path('',views.CartPage,name = 'cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name = 'add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.remove_cart,name = 'remove_cart'),
    path('remove_item_cart/<int:product_id>/<int:cart_item_id>/',views.remove_item_cart,name = 'remove_item_cart'),
    path('checkout/',views.checkout,name = 'checkout'),


]