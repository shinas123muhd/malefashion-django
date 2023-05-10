from . import views
from django.urls import path

urlpatterns = [
    path("place_order/", views.PlaceOrder, name="placeorder"),
    path("confirm_order/<int:order_number>/", views.ConfirmOrder, name="confirmorder"),
    path("cod_complete/", views.CodComplete, name="codcomplete"),
    path("paypal/", views.Paypalpay, name="paypal"),
    path("cod/", views.Codpay, name="cod"),   
    path("order_complete/", views.order_complete, name="order_complete"),
]
