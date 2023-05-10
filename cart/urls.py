from django.urls import path
from . import views


urlpatterns = [
    path("", views.CartPage, name="cart"),
    path("add_cart/<int:product_id>/", views.add_cart, name="add_cart"),
    path("plus_cart", views.plus_cart, name="plus_cart"),
    path("remove_cart", views.remove_cart, name="remove_cart"),
    path("remove_item_cart/<int:id>/", views.remove_item_cart, name="remove_item_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("wishlist/", views.wishlist_Page, name="wishlist"),
    path("addwish/<int:product_id>/", views.addwish, name="addwish"),
    path("removewish/<int:product_id>/", views.removewish, name="removewish"),
    path("applycoupon/", views.applycoupon, name="applycoupon"),
]
